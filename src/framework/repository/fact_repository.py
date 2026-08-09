from datetime import datetime

from sqlalchemy import select

from src.database.database import SessionLocal
from src.database.models import (
    DimDate,
    DimSource,
    FactArticle,
)


class FactRepository:

    def save_articles(
        self,
        articles,
    ):
        db = SessionLocal()

        try:

            inserted = 0

            for article in articles:

                published_at = article[
                    "published_at"
                ]

                if not published_at:
                    continue

                if isinstance(
                    published_at,
                    str,
                ):
                    published_date = (
                        datetime.fromisoformat(
                            published_at
                        ).date()
                    )

                else:
                    published_date = published_at

                source = db.scalar(
                    select(DimSource).where(
                        DimSource.source_name
                        == article["source"]
                    )
                )

                if source is None:
                    continue

                date_key = int(
                    published_date.strftime(
                        "%Y%m%d"
                    )
                )

                date_dimension = db.scalar(
                    select(DimDate).where(
                        DimDate.date_key
                        == date_key
                    )
                )

                if date_dimension is None:
                    continue

                existing_fact = db.scalar(
                    select(FactArticle).where(
                        FactArticle.headline
                        == article["headline"],
                        FactArticle.published_at
                        == published_date,
                        FactArticle.source_key
                        == source.source_key,
                    )
                )

                if existing_fact is not None:
                    continue

                fact = FactArticle(
                    date_key=date_dimension.date_key,
                    source_key=source.source_key,
                    category_key=None,
                    headline=article["headline"],
                    published_at=published_date,
                    loaded_at=datetime.now(),
                )

                db.add(fact)

                inserted += 1

            db.commit()

            return inserted

        except Exception:

            db.rollback()

            raise

        finally:

            db.close()