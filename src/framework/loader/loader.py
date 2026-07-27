from src.framework.repository.article_repository import ArticleRepository


class Loader:

    def load(self, articles):
        print("Loading articles...")

        repository = ArticleRepository()
        repository.save_articles(articles)

        print(f"Inserted {len(articles)} articles into PostgreSQL.")