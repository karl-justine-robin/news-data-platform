from datetime import datetime

from src.framework.logging.logger import logger
from src.framework.repository.dimension_repository import (
    DimensionRepository,
)


class DimensionLoader:

    def __init__(self):

        self.repository = DimensionRepository()

    def load_sources(
        self,
        sources,
    ):

        logger.info(
            "Loading source dimension..."
        )

        inserted = (
            self.repository.save_sources(
                sources
            )
        )

        logger.info(
            "Inserted %d new source(s) into dim_source.",
            inserted,
        )

        return inserted

    def load_categories(
        self,
        categories,
    ):

        logger.info(
            "Loading category dimension..."
        )

        inserted = (
            self.repository.save_categories(
                categories
            )
        )

        logger.info(
            "Inserted %d new category(s) into dim_category.",
            inserted,
        )

        return inserted

    def load_dates(
        self,
        dates,
    ):

        logger.info(
            "Loading date dimension..."
        )

        parsed_dates = set()

        for value in dates:

            if isinstance(value, str):

                parsed_date = (
                    datetime.fromisoformat(
                        value
                    ).date()
                )

            else:

                parsed_date = value

            parsed_dates.add(
                parsed_date
            )

        inserted = (
            self.repository.save_dates(
                parsed_dates
            )
        )

        logger.info(
            "Inserted %d new date(s) into dim_date.",
            inserted,
        )

        return inserted