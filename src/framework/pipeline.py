from time import perf_counter

from src.framework.collector.collector import Collector
from src.framework.error.exceptions import PipelineException
from src.framework.loader.loader import Loader
from src.framework.logging.logger import logger
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

    def run(self):

        start_time = perf_counter()

        logger.info("Starting pipeline...")

        run_id = self.tracker.start()

        try:

            feed = self.collector.collect()

            self.schema_validator.validate(feed)

            preprocessed_feed = self.preprocessor.preprocess(
                feed
            )

            transformed_articles = self.transformer.transform(
                preprocessed_feed
            )

            validation_result = self.validator.validate(
                transformed_articles
            )

            self.loader.load(
                validation_result.valid_articles
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