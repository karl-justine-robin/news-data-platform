from datetime import datetime

import psycopg

from config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


class PipelineRunRepository:

    def start_run(self, pipeline_name):

        with psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        ) as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    INSERT INTO pipeline_runs (
                        pipeline_name,
                        status,
                        start_time,
                        end_time,
                        duration_seconds,
                        records_processed,
                        error_message
                    )
                    VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    RETURNING id;
                    """,
                    (
                        pipeline_name,
                        "RUNNING",
                        datetime.now(),
                        None,
                        0,
                        0,
                        None,
                    ),
                )

                run_id = cursor.fetchone()[0]

            connection.commit()

        return run_id

    def finish_run(
        self,
        run_id,
        success,
        records_processed,
        error_message=None,
    ):

        end_time = datetime.now()

        with psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        ) as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT start_time
                    FROM pipeline_runs
                    WHERE id = %s;
                    """,
                    (run_id,),
                )

                row = cursor.fetchone()

                if row is None:
                    return

                start_time = row[0]

                duration = (
                    end_time - start_time
                ).total_seconds()

                cursor.execute(
                    """
                    UPDATE pipeline_runs
                    SET
                        status = %s,
                        end_time = %s,
                        duration_seconds = %s,
                        records_processed = %s,
                        error_message = %s
                    WHERE id = %s;
                    """,
                    (
                        "SUCCESS" if success else "FAILED",
                        end_time,
                        duration,
                        records_processed,
                        error_message,
                        run_id,
                    ),
                )

            connection.commit()