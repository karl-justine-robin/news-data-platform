from datetime import datetime

import psycopg

from config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


class QualityRunRepository:

    def save(self, metrics):

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
                    INSERT INTO quality_runs (
                        total_records,
                        valid_records,
                        invalid_records,
                        missing_headline,
                        missing_body,
                        missing_source,
                        invalid_date,
                        quality_score,
                        created_at
                    )
                    VALUES (
                        %s,
                        %s,
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
                        metrics.total_records,
                        metrics.valid_records,
                        metrics.invalid_records,
                        metrics.missing_headline,
                        metrics.missing_body,
                        metrics.missing_source,
                        metrics.invalid_date,
                        metrics.quality_score,
                        datetime.now(),
                    ),
                )

                quality_run_id = cursor.fetchone()[0]

            connection.commit()

        return quality_run_id


    def get_latest(self):

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
                    SELECT
                        total_records,
                        valid_records,
                        invalid_records,
                        missing_headline,
                        missing_body,
                        missing_source,
                        invalid_date,
                        quality_score
                    FROM quality_runs
                    ORDER BY created_at DESC
                    LIMIT 1;
                    """
                )

                row = cursor.fetchone()

        if row is None:
            return None

        return {
            "total_records": row[0],
            "valid_records": row[1],
            "invalid_records": row[2],
            "missing_headline": row[3],
            "missing_body": row[4],
            "missing_source": row[5],
            "invalid_date": row[6],
            "quality_score": row[7],
        }