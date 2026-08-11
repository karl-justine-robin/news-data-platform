from time import perf_counter

from src.framework.logging.logger import logger


class StageTimer:

    def __init__(self, stage_name: str):

        self.stage_name = stage_name
        self.start_time = None

    def start(self):

        self.start_time = perf_counter()

        logger.info(
            "[%s] Starting",
            self.stage_name,
        )

    def finish(self, **metrics):

        elapsed = (
            perf_counter() - self.start_time
        )

        metric_text = " | ".join(
            f"{key}={value}"
            for key, value in metrics.items()
        )

        if metric_text:

            logger.info(
                "[%s] Completed | %s | duration=%.2fs",
                self.stage_name,
                metric_text,
                elapsed,
            )

        else:

            logger.info(
                "[%s] Completed | duration=%.2fs",
                self.stage_name,
                elapsed,
            )

        return elapsed

    def fail(self, error):

        elapsed = (
            perf_counter() - self.start_time
        )

        logger.error(
            "[%s] FAILED | duration=%.2fs | error=%s",
            self.stage_name,
            elapsed,
            error,
        )

        return elapsed