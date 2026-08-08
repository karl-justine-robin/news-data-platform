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
from src.framework.medallion.bronze_writer import BronzeWriter
from src.framework.medallion.gold_writer import GoldWriter
from src.framework.medallion.silver_writer import SilverWriter
from src.framework.preprocessor.preprocessor import Preprocessor
from src.framework.quality.quality_service import QualityService
from src.framework.schema.schema_validator import SchemaValidator
from src.framework.tracker.run_tracker import RunTracker
from src.framework.transformer.transformer import Transformer
from src.framework.validator.validator import Validator


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

    def run(self):

        start_time = perf_counter()

        logger.info("Starting pipeline...")

        run_id = self.tracker.start()

        try:

            feed = self.collector.collect()

            bronze_timestamp = self.bronze_writer.write(
                feed
            )

            logger.info(
                "Bronze layer written at %s.",
                bronze_timestamp,
            )

            self.schema_validator.validate(
                feed
            )

            preprocessed_feed = (
                self.preprocessor.preprocess(
                    feed
                )
            )

            transformed_articles = (
                self.transformer.transform(
                    preprocessed_feed
                )
            )

            incremental_result = (
                self.incremental_filter.filter(
                    transformed_articles
                )
            )

            validation_result = (
                self.validator.validate(
                    incremental_result.new_articles
                )
            )

            silver_file = (
                self.silver_writer.write(
                    validation_result.valid_articles,
                    bronze_timestamp,
                )
            )

            logger.info(
                "Silver layer written to %s.",
                silver_file,
            )

            gold_files = self.gold_writer.write(
                validation_result.valid_articles,
                validation_result.metrics,
                bronze_timestamp,
            )

            logger.info(
                "Gold datasets created:"
            )

            for gold_file in gold_files:
                logger.info(
                    "  %s",
                    gold_file,
                )

            self.loader.load(
                validation_result.valid_articles
            )

            self.watermark_service.update_many(
                incremental_result.latest_watermarks
            )

            logger.info(
                "Updated %d watermark(s).",
                len(
                    incremental_result.latest_watermarks
                ),
            )

            logger.info(
                self.quality_service.generate_report(
                    validation_result.metrics
                )
            )

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

            logger.error(str(error))

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

        elapsed = perf_counter() - start_time

        logger.info("Pipeline finished.")

        logger.info(
            "Execution time: %.2f seconds.",
            elapsed,
        )