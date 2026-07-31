from src.framework.logging.logger import logger
from src.framework.repository.pipeline_run_repository import (
    PipelineRunRepository,
)
from config import PIPELINE_NAME


class RunTracker:

    def __init__(self):
        self.repository = PipelineRunRepository()
        self.run = None

    def start(self):
        self.run = self.repository.start_run(
            pipeline_name=PIPELINE_NAME
        )

        logger.info(
            f"Pipeline started at {self.run.start_time}"
        )

        return self.run
    

    def finish(
        self,
        run,
        records_processed,
        success=True,
        error_message=None,
    ):
        self.repository.finish_run(
            run=run,
            success=success,
            records_processed=records_processed,
            error_message=error_message,
        )

        logger.info(
            f"""
    Pipeline Run Summary
    --------------------
    Status: {run.status}
    Started: {run.start_time}
    Finished: {run.end_time}
    Duration: {run.duration_seconds:.4f}s
    Records: {run.records_processed}
    """
        )

        self.repository.close()