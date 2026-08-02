from datetime import datetime

from config import PIPELINE_NAME
from src.framework.logging.logger import logger
from src.framework.repository.pipeline_run_repository import (
    PipelineRunRepository,
)


class RunTracker:

    def __init__(self):
        self.repository = PipelineRunRepository()
        self.run_id = None
        self.start_time = None

    def start(self):

        self.start_time = datetime.now()

        self.run_id = self.repository.start_run(
            pipeline_name=PIPELINE_NAME,
        )

        logger.info(
            "Pipeline started at %s",
            self.start_time,
        )

        return self.run_id

    def finish(
        self,
        run_id,
        records_processed,
        success=True,
        error_message=None,
    ):

        end_time = datetime.now()

        duration = (
            end_time - self.start_time
        ).total_seconds()

        self.repository.finish_run(
            run_id=run_id,
            success=success,
            records_processed=records_processed,
            error_message=error_message,
        )

        logger.info(
            f"""
    Pipeline Run Summary
    --------------------
    Status: {"SUCCESS" if success else "FAILED"}
    Started: {self.start_time}
    Finished: {end_time}
    Duration: {duration:.4f}s
    Records: {records_processed}
    """
        )