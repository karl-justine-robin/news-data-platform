from src.database.database import SessionLocal
from src.database.models import Article
from src.framework.logging.logger import logger
from src.framework.repository.dimension_repository import (
    DimensionRepository,
)
from src.framework.repository.fact_repository import (
    FactRepository,
)


class WarehouseBackfill:

    def __init__(self):

        self.dimension_repository = (
            DimensionRepository()
        )

        self.fact_repository = (
            FactRepository()
        )

    def run(self):

        logger.info(
            "Starting warehouse backfill..."
        )

        db = SessionLocal()

        try:

            articles = db.query(
                Article
            ).all()

        finally:

            db.close()

        if not articles:

            logger.info(
                "No articles available for warehouse backfill."
            )

            return 0

        sources = {
            article.source
            for article in articles
            if article.source
        }

        dates = {
            article.published_at
            for article in articles
            if article.published_at
        }

        self.dimension_repository.save_sources(
            sources
        )

        self.dimension_repository.save_dates(
            dates
        )

        article_data = [
            {
                "headline": article.headline,
                "published_at": article.published_at,
                "source": article.source,
                "loaded_at": article.loaded_at,
            }
            for article in articles
        ]

        inserted = (
            self.fact_repository.save_articles(
                article_data
            )
        )

        logger.info(
            "Warehouse backfill completed. "
            "Inserted %d fact article(s).",
            inserted,
        )

        return inserted