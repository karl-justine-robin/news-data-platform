from src.framework.logging.logger import logger


class Preprocessor:

    def preprocess(self, feed):
        logger.info("Preprocessing feed...")

        # No preprocessing logic yet
        preprocessed_feed = feed

        logger.info("Preprocessing completed.")

        return preprocessed_feed