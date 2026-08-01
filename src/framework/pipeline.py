from time import perf_counter

from src.framework.logging.logger import logger

from src.framework.collector.collector import Collector
from src.framework.preprocessor.preprocessor import Preprocessor
from src.framework.transformer.transformer import Transformer
from src.framework.validator.validator import Validator
from src.framework.loader.loader import Loader
from src.framework.tracker.run_tracker import RunTracker
from src.framework.schema.schema_validator import SchemaValidator
from src.framework.error.exceptions import PipelineException


class Pipeline:

    def __init__(self):
        self.collector = Collector()
        self.schema_validator = SchemaValidator()
        self.preprocessor = Preprocessor()
        self.transformer = Transformer()
        self.validator = Validator()
        self.loader = Loader()
        self.tracker = RunTracker()

    def run(self):
        start_time = perf_counter()

        logger.info("Starting pipeline...")

        run = self.tracker.start()

        try:
            feed = self.collector.collect()

            self.schema_validator.validate(feed)

            preprocessed_feed = self.preprocessor.preprocess(feed)

            transformed_articles = self.transformer.transform(
                preprocessed_feed
            )

            validated_articles = self.validator.validate(
                transformed_articles
            )

            self.loader.load(validated_articles)

            records = len(validated_articles)

            logger.info(
                f"Processed {records} standardized article(s)."
            )

            self.tracker.finish(
                run=run,
                records_processed=records,
                success=True,
            )

        except PipelineException as error:

            logger.error(str(error))

            self.tracker.finish(
                run=run,
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
                run=run,
                records_processed=0,
                success=False,
                error_message=str(error),
            )

            raise

        elapsed = perf_counter() - start_time

        logger.info("Pipeline finished.")
        logger.info(
            f"Execution time: {elapsed:.2f} seconds."
        )