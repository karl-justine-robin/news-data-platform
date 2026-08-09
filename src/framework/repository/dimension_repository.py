from sqlalchemy import select

from src.database.database import SessionLocal
from src.database.models import DimSource
from src.database.models import (
    DimCategory,
    DimDate,
    DimSource,
)


class DimensionRepository:

    def save_sources(
        self,
        sources,
    ):
        db = SessionLocal()

        try:

            inserted = 0

            existing_sources = {
                source.source_name
                for source in db.scalars(
                    select(DimSource)
                ).all()
            }

            for source_name in sources:

                if source_name in existing_sources:
                    continue

                db.add(
                    DimSource(
                        source_name=source_name
                    )
                )

                inserted += 1

            db.commit()

            return inserted

        except Exception:

            db.rollback()

            raise

        finally:

            db.close()


    def save_categories(
        self,
        categories,
    ):
        db = SessionLocal()

        try:

            inserted = 0

            existing_categories = {
                category.category_name
                for category in db.scalars(
                    select(DimCategory)
                ).all()
            }

            for category_name in categories:

                if category_name in existing_categories:
                    continue

                db.add(
                    DimCategory(
                        category_name=category_name
                    )
                )

                inserted += 1

            db.commit()

            return inserted

        except Exception:

            db.rollback()

            raise

        finally:

            db.close()



    def save_dates(
        self,
        dates,
    ):
        db = SessionLocal()

        try:

            inserted = 0

            existing_dates = {
                date.full_date
                for date in db.scalars(
                    select(DimDate)
                ).all()
            }

            for current_date in dates:

                if current_date in existing_dates:
                    continue

                date_key = int(
                    current_date.strftime("%Y%m%d")
                )

                db.add(
                    DimDate(
                        date_key=date_key,
                        full_date=current_date,
                        year=current_date.year,
                        month=current_date.month,
                        month_name=current_date.strftime(
                            "%B"
                        ),
                        day=current_date.day,
                        day_of_week=current_date.strftime(
                            "%A"
                        ),
                    )
                )

                inserted += 1

            db.commit()

            return inserted

        except Exception:

            db.rollback()

            raise

        finally:

            db.close()