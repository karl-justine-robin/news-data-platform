from src.framework.logging.logger import logger
from src.framework.repository.fact_repository import (
    FactRepository,
)


class FactLoader:

    def __init__(self):

        self.repository = FactRepository()

    def load_articles(
        self,
        articles,
    ):

        logger.info(
            "Loading article fact table..."
        )

        inserted = (
            self.repository.save_articles(
                articles
            )
        )

        logger.info(
            "Inserted %d article(s) into fact_article.",
            inserted,
        )

        return inserted