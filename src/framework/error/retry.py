import time

from src.framework.logging.logger import logger


def retry(
    func,
    *args,
    max_attempts=3,
    delay=2,
    exceptions=(Exception,),
    **kwargs,
):
    """
    Retry a function if it raises one of the specified exceptions.
    """

    attempt = 1

    while attempt <= max_attempts:

        try:
            return func(*args, **kwargs)

        except exceptions as error:

            logger.warning(
                f"Attempt {attempt}/{max_attempts} failed: {error}"
            )

            if attempt == max_attempts:
                logger.error(
                    f"Maximum retry attempts reached for {func.__name__}"
                )
                raise

            logger.info(
                f"Retrying in {delay} second(s)..."
            )

            time.sleep(delay)

            attempt += 1