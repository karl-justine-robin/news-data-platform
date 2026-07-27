from src.framework.logging.logger import logger
from src.framework.repository.article_repository import ArticleRepository


class Loader:

    def load(self, articles):
        logger.info("Loading articles...")

        repository = ArticleRepository()
        inserted = repository.save_articles(articles)

        logger.info(
            f"Inserted {inserted} new article(s) into PostgreSQL."
        )