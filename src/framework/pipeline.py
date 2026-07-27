from time import perf_counter

from src.framework.logging.logger import logger

from src.framework.collector.collector import Collector
from src.framework.preprocessor.preprocessor import Preprocessor
from src.framework.transformer.transformer import Transformer
from src.framework.validator.validator import Validator
from src.framework.loader.loader import Loader


class Pipeline:

    def __init__(self):
        self.collector = Collector()
        self.preprocessor = Preprocessor()
        self.transformer = Transformer()
        self.validator = Validator()
        self.loader = Loader()

    def run(self):
        start_time = perf_counter()

        logger.info("Starting pipeline...")

        feed = self.collector.collect()

        preprocessed_feed = self.preprocessor.preprocess(feed)

        transformed_articles = self.transformer.transform(preprocessed_feed)

        validated_articles = self.validator.validate(transformed_articles)

        self.loader.load(validated_articles)

        logger.info(
            f"Processed {len(validated_articles)} standardized article(s)."
        )

        elapsed = perf_counter() - start_time

        logger.info("Pipeline finished.")
        logger.info(f"Execution time: {elapsed:.2f} seconds.")