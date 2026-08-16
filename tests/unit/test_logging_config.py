import logging

from src.framework.logging.logging_config import configure_logger


def test_configure_logger_returns_existing_logger():

    logger = logging.getLogger("test_existing_logger")

    handler = logging.StreamHandler()
    logger.addHandler(handler)

    try:
        result = configure_logger(
            "test_existing_logger",
            "test.log",
        )

        assert result is logger
        assert logger.handlers == [handler]

    finally:
        logger.removeHandler(handler)
        handler.close()