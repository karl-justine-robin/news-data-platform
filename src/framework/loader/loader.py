from src.framework.repository.article_repository import ArticleRepository


class Loader:

    def load(self, articles):
        print("Loading articles...")

        repository = ArticleRepository()
        inserted = repository.save_articles(articles)

        print(f"Inserted {inserted} new article(s) into PostgreSQL.")