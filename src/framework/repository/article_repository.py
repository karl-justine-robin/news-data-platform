from datetime import datetime

import psycopg

from config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


class ArticleRepository:

    def save_articles(self, articles):

        with psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        ) as connection:

            with connection.cursor() as cursor:

                inserted = 0

                for article in articles:

                    cursor.execute(
                        """
                        INSERT INTO articles (
                            headline,
                            published_at,
                            body,
                            source,
                            loaded_at
                        )
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (
                            headline,
                            published_at,
                            source
                        )
                        DO NOTHING;
                        """,
                        (
                            article["headline"],
                            article["published_at"],
                            article["body"],
                            article["source"],      # <-- Use source from the article
                            datetime.now(),
                        ),
                    )

                    inserted += cursor.rowcount

            connection.commit()

        return inserted