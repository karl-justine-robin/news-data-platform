from datetime import datetime

from api.app.database import SessionLocal
from api.app.models import PipelineRun


class PipelineRunRepository:

    def __init__(self):
        self.db = SessionLocal()

    def start_run(self, pipeline_name):
        run = PipelineRun(
            pipeline_name=pipeline_name,
            status="RUNNING",
            start_time=datetime.now(),
            end_time=None,
            duration_seconds=0,
            records_processed=0,
            error_message=None,
        )

        self.db.add(run)
        self.db.commit()
        self.db.refresh(run)

        return run

    def finish_run(
        self,
        run,
        success,
        records_processed,
        error_message=None,
    ):
        end_time = datetime.now()

        run.end_time = end_time
        run.status = "SUCCESS" if success else "FAILED"
        run.records_processed = records_processed
        run.error_message = error_message

        run.duration_seconds = (
            end_time - run.start_time
        ).total_seconds()

        self.db.commit()
        self.db.refresh(run)

    def close(self):
        self.db.close()