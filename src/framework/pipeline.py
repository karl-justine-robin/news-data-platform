from time import perf_counter

from config import (
    ENABLE_BRONZE,
    ENABLE_GOLD,
    ENABLE_INCREMENTAL,
    ENABLE_SILVER,
    ENABLE_WAREHOUSE,
)

from src.framework.collector.collector import Collector
from src.framework.error.exceptions import PipelineException

from src.framework.incremental.incremental_filter import (
    IncrementalFilter,
)
from src.framework.incremental.incremental_result import (
    IncrementalResult,
)
from src.framework.incremental.watermark_service import (
    WatermarkService,
)

from src.framework.loader.loader import Loader
from src.framework.logging.logger import logger
from src.framework.logging.stage_timer import StageTimer

from src.framework.medallion.bronze_writer import BronzeWriter
from src.framework.medallion.gold_writer import GoldWriter
from src.framework.medallion.silver_writer import SilverWriter

from src.framework.preprocessor.preprocessor import Preprocessor
from src.framework.quality.quality_service import QualityService
from src.framework.schema.schema_validator import SchemaValidator
from src.framework.tracker.run_tracker import RunTracker
from src.framework.transformer.transformer import Transformer
from src.framework.validator.validator import Validator

from src.framework.warehouse.dimension_loader import (
    DimensionLoader,
)
from src.framework.warehouse.fact_loader import (
    FactLoader,
)


class Pipeline:

    def __init__(self):

        self.collector = Collector()
        self.schema_validator = SchemaValidator()
        self.preprocessor = Preprocessor()
        self.transformer = Transformer()
        self.validator = Validator()
        self.loader = Loader()
        self.tracker = RunTracker()
        self.quality_service = QualityService()

        self.bronze_writer = BronzeWriter()
        self.silver_writer = SilverWriter()
        self.gold_writer = GoldWriter()

        self.incremental_filter = IncrementalFilter()
        self.watermark_service = WatermarkService()

        self.dimension_loader = DimensionLoader()
        self.fact_loader = FactLoader()

    def _run_bronze(self, feed):

        if not ENABLE_BRONZE:

            logger.info(
                "Bronze layer disabled."
            )

            return None

        bronze_timestamp = (
            self.bronze_writer.write(
                feed
            )
        )

        logger.info(
            "Bronze layer written at %s.",
            bronze_timestamp,
        )

        return bronze_timestamp

    def _run_incremental(
        self,
        transformed_articles,
    ):

        if ENABLE_INCREMENTAL:

            incremental_result = (
                self.incremental_filter.filter(
                    transformed_articles
                )
            )

            logger.info(
                "Incremental filtering enabled."
            )

            return incremental_result

        logger.info(
            "Incremental filtering disabled."
        )

        return IncrementalResult(
            new_articles=transformed_articles,
            latest_watermarks={},
        )

    def _run_silver(
        self,
        valid_articles,
        bronze_timestamp,
    ):

        if not ENABLE_SILVER:

            logger.info(
                "Silver layer disabled."
            )

            return None

        silver_file = (
            self.silver_writer.write(
                valid_articles,
                bronze_timestamp,
            )
        )

        logger.info(
            "Silver layer written to %s.",
            silver_file,
        )

        return silver_file

    def _run_gold(
        self,
        valid_articles,
        metrics,
        bronze_timestamp,
    ):

        if not ENABLE_GOLD:

            logger.info(
                "Gold layer disabled."
            )

            return []

        gold_files = (
            self.gold_writer.write(
                valid_articles,
                metrics,
                bronze_timestamp,
            )
        )

        logger.info(
            "Gold datasets created:"
        )

        for gold_file in gold_files:

            logger.info(
                "  %s",
                gold_file,
            )

        return gold_files

    def _run_warehouse(
        self,
        valid_articles,
    ):

        if not ENABLE_WAREHOUSE:

            logger.info(
                "Warehouse loading disabled."
            )

            return

        warehouse_timer = StageTimer(
            "WAREHOUSE"
        )

        warehouse_timer.start()

        self.loader.load(
            valid_articles
        )

        self.fact_loader.load_articles(
            valid_articles
        )

        warehouse_timer.finish(
            articles=len(
                valid_articles
            ),
        )

    def _run_dimensions(
        self,
        valid_articles,
    ):

        sources = {
            article["source"]
            for article in valid_articles
        }

        dates = {
            article["published_at"]
            for article in valid_articles
        }

        self.dimension_loader.load_sources(
            sources
        )

        self.dimension_loader.load_dates(
            dates
        )

        logger.info(
            "Loaded %d source dimension(s) and "
            "%d date dimension(s).",
            len(sources),
            len(dates),
        )

    def _update_watermarks(
        self,
        incremental_result,
    ):

        if not ENABLE_INCREMENTAL:

            logger.info(
                "Watermark update skipped because "
                "incremental processing is disabled."
            )

            return

        self.watermark_service.update_many(
            incremental_result.latest_watermarks
        )

        logger.info(
            "Updated %d watermark(s).",
            len(
                incremental_result.latest_watermarks
            ),
        )

    def _run_quality_report(
        self,
        metrics,
    ):

        report = (
            self.quality_service.generate_report(
                metrics
            )
        )

        logger.info(
            report
        )

        return report

    def _finish_run(
        self,
        run_id,
        records_processed,
        success=True,
        error_message=None,
    ):

        self.tracker.finish(
            run_id=run_id,
            records_processed=records_processed,
            success=success,
            error_message=error_message,
        )

    def run(self):

        start_time = perf_counter()

        logger.info(
            "Starting pipeline..."
        )

        run_id = self.tracker.start()

        try:

            # =========================================
            # Collect
            # =========================================

            collect_timer = StageTimer(
                "COLLECT"
            )

            collect_timer.start()

            feed = self.collector.collect()

            collect_timer.finish(
                feeds=len(feed),
            )

            # =========================================
            # Bronze
            # =========================================

            bronze_timestamp = (
                self._run_bronze(
                    feed
                )
            )

            # =========================================
            # Schema Validation
            # =========================================

            self.schema_validator.validate(
                feed
            )

            # =========================================
            # Preprocess
            # =========================================

            preprocessed_feed = (
                self.preprocessor.preprocess(
                    feed
                )
            )

            # =========================================
            # Transform
            # =========================================

            transform_timer = StageTimer(
                "TRANSFORM"
            )

            transform_timer.start()

            transformed_articles = (
                self.transformer.transform(
                    preprocessed_feed
                )
            )

            transform_timer.finish(
                articles=len(
                    transformed_articles
                ),
            )

            # =========================================
            # Incremental Processing
            # =========================================

            incremental_result = (
                self._run_incremental(
                    transformed_articles
                )
            )

            # =========================================
            # Validation
            # =========================================

            validate_timer = StageTimer(
                "VALIDATE"
            )

            validate_timer.start()

            validation_result = (
                self.validator.validate(
                    incremental_result.new_articles
                )
            )

            validate_timer.finish(
                valid=len(
                    validation_result.valid_articles
                ),
                invalid=len(
                    validation_result.invalid_articles
                ),
            )

            # =========================================
            # Dimensions
            # =========================================

            self._run_dimensions(
                validation_result.valid_articles
            )

            # =========================================
            # Silver
            # =========================================

            self._run_silver(
                validation_result.valid_articles,
                bronze_timestamp,
            )

            # =========================================
            # Gold
            # =========================================

            self._run_gold(
                validation_result.valid_articles,
                validation_result.metrics,
                bronze_timestamp,
            )

            # =========================================
            # Warehouse
            # =========================================

            self._run_warehouse(
                validation_result.valid_articles
            )

            # =========================================
            # Watermark
            # =========================================

            self._update_watermarks(
                incremental_result
            )

            # =========================================
            # Quality
            # =========================================

            self._run_quality_report(
                validation_result.metrics
            )

            # =========================================
            # Records
            # =========================================

            records = len(
                validation_result.valid_articles
            )

            logger.info(
                "Processed %d standardized article(s).",
                records,
            )

            # =========================================
            # Tracker
            # =========================================

            self._finish_run(
                run_id=run_id,
                records_processed=records,
            )

        except PipelineException as error:

            logger.error(
                str(error)
            )

            self._finish_run(
                run_id=run_id,
                records_processed=0,
                success=False,
                error_message=str(error),
            )

            raise

        except Exception as error:

            logger.exception(
                "Unexpected pipeline error."
            )

            self._finish_run(
                run_id=run_id,
                records_processed=0,
                success=False,
                error_message=str(error),
            )

            raise

        elapsed = (
            perf_counter()
            - start_time
        )

        logger.info(
            "Pipeline finished."
        )

        logger.info(
            "Execution time: %.2f seconds.",
            elapsed,
        )