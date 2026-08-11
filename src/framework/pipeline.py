from time import perf_counter

from src.framework.collector.collector import Collector
from src.framework.error.exceptions import PipelineException
from src.framework.incremental.incremental_filter import (
    IncrementalFilter,
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

    def run(self):

        start_time = perf_counter()

        logger.info(
            "Starting pipeline..."
        )

        run_id = self.tracker.start()

        try:

            # ---------------------------------
            # Collect
            # ---------------------------------

            collect_timer = StageTimer("COLLECT")

            collect_timer.start()

            try:

                feed = self.collector.collect()

            except Exception as error:

                collect_timer.fail(error)

                raise

            collect_timer.finish(
                feeds=len(feed),
            )

            # ---------------------------------
            # Bronze
            # ---------------------------------

            bronze_timer = StageTimer("BRONZE")

            bronze_timer.start()

            try:

                bronze_timestamp = (
                    self.bronze_writer.write(
                        feed
                    )
                )

            except Exception as error:

                bronze_timer.fail(error)

                raise

            bronze_timer.finish()

            logger.info(
                "Bronze layer written at %s.",
                bronze_timestamp,
            )

            # ---------------------------------
            # Schema Validation
            # ---------------------------------

            schema_timer = StageTimer("SCHEMA")

            schema_timer.start()

            try:

                self.schema_validator.validate(
                    feed
                )

            except Exception as error:

                schema_timer.fail(error)

                raise

            schema_timer.finish()

            # ---------------------------------
            # Preprocess
            # ---------------------------------

            preprocess_timer = StageTimer(
                "PREPROCESS"
            )

            preprocess_timer.start()

            try:

                preprocessed_feed = (
                    self.preprocessor.preprocess(
                        feed
                    )
                )

            except Exception as error:

                preprocess_timer.fail(error)

                raise

            preprocess_timer.finish(
                feeds=len(preprocessed_feed),
            )

            # ---------------------------------
            # Transform
            # ---------------------------------

            transform_timer = StageTimer(
                "TRANSFORM"
            )

            transform_timer.start()

            try:

                transformed_articles = (
                    self.transformer.transform(
                        preprocessed_feed
                    )
                )

            except Exception as error:

                transform_timer.fail(error)

                raise

            transform_timer.finish(
                articles=len(
                    transformed_articles
                ),
            )

            # ---------------------------------
            # Incremental Filter
            # ---------------------------------

            incremental_timer = StageTimer(
                "INCREMENTAL"
            )

            incremental_timer.start()

            try:

                incremental_result = (
                    self.incremental_filter.filter(
                        transformed_articles
                    )
                )

            except Exception as error:

                incremental_timer.fail(error)

                raise

            incremental_timer.finish(
                new_articles=len(
                    incremental_result.new_articles
                ),
            )

            # ---------------------------------
            # Validation
            # ---------------------------------

            validate_timer = StageTimer(
                "VALIDATE"
            )

            validate_timer.start()

            try:

                validation_result = (
                    self.validator.validate(
                        incremental_result.new_articles
                    )
                )

            except Exception as error:

                validate_timer.fail(error)

                raise

            validate_timer.finish(
                valid=len(
                    validation_result.valid_articles
                ),
                invalid=len(
                    validation_result.invalid_articles
                ),
            )

            # ---------------------------------
            # Dimensions
            # ---------------------------------

            sources = {
                article["source"]
                for article
                in validation_result.valid_articles
            }

            dates = {
                article["published_at"]
                for article
                in validation_result.valid_articles
            }

            dimension_timer = StageTimer(
                "DIMENSIONS"
            )

            dimension_timer.start()

            try:

                self.dimension_loader.load_sources(
                    sources
                )

                self.dimension_loader.load_dates(
                    dates
                )

            except Exception as error:

                dimension_timer.fail(error)

                raise

            dimension_timer.finish(
                sources=len(sources),
                dates=len(dates),
            )

            # ---------------------------------
            # Silver
            # ---------------------------------

            silver_timer = StageTimer(
                "SILVER"
            )

            silver_timer.start()

            try:

                silver_file = (
                    self.silver_writer.write(
                        validation_result.valid_articles,
                        bronze_timestamp,
                    )
                )

            except Exception as error:

                silver_timer.fail(error)

                raise

            silver_timer.finish(
                articles=len(
                    validation_result.valid_articles
                ),
            )

            logger.info(
                "Silver layer written to %s.",
                silver_file,
            )

            # ---------------------------------
            # Gold
            # ---------------------------------

            gold_timer = StageTimer("GOLD")

            gold_timer.start()

            try:

                gold_files = (
                    self.gold_writer.write(
                        validation_result.valid_articles,
                        validation_result.metrics,
                        bronze_timestamp,
                    )
                )

            except Exception as error:

                gold_timer.fail(error)

                raise

            gold_timer.finish(
                files=len(gold_files),
            )

            logger.info(
                "Gold datasets created:"
            )

            for gold_file in gold_files:

                logger.info(
                    "  %s",
                    gold_file,
                )

            # ---------------------------------
            # Warehouse
            # ---------------------------------

            warehouse_timer = StageTimer(
                "WAREHOUSE"
            )

            warehouse_timer.start()

            try:

                self.loader.load(
                    validation_result.valid_articles
                )

                self.fact_loader.load_articles(
                    validation_result.valid_articles
                )

            except Exception as error:

                warehouse_timer.fail(error)

                raise

            warehouse_timer.finish(
                articles=len(
                    validation_result.valid_articles
                ),
            )

            # ---------------------------------
            # Watermark
            # ---------------------------------

            watermark_timer = StageTimer(
                "WATERMARK"
            )

            watermark_timer.start()

            try:

                self.watermark_service.update_many(
                    incremental_result.latest_watermarks
                )

            except Exception as error:

                watermark_timer.fail(error)

                raise

            watermark_timer.finish(
                sources=len(
                    incremental_result.latest_watermarks
                ),
            )

            logger.info(
                "Updated %d watermark(s).",
                len(
                    incremental_result.latest_watermarks
                ),
            )

            # ---------------------------------
            # Quality
            # ---------------------------------

            quality_timer = StageTimer(
                "QUALITY"
            )

            quality_timer.start()

            try:

                quality_report = (
                    self.quality_service.generate_report(
                        validation_result.metrics
                    )
                )

            except Exception as error:

                quality_timer.fail(error)

                raise

            quality_timer.finish(
                quality_score=(
                    validation_result.metrics.quality_score
                ),
            )

            logger.info(
                quality_report
            )

            # ---------------------------------
            # Pipeline Summary
            # ---------------------------------

            records = len(
                validation_result.valid_articles
            )

            logger.info(
                "Processed %d standardized article(s).",
                records,
            )

            self.tracker.finish(
                run_id=run_id,
                records_processed=records,
            )

        except PipelineException as error:

            logger.error(
                str(error)
            )

            self.tracker.finish(
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

            self.tracker.finish(
                run_id=run_id,
                records_processed=0,
                success=False,
                error_message=str(error),
            )

            raise

        elapsed = (
            perf_counter() - start_time
        )

        logger.info(
            "Pipeline finished."
        )

        logger.info(
            "Execution time: %.2f seconds.",
            elapsed,
        )