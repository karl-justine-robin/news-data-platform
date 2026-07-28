from sqlalchemy.orm import Session

from app.enums import ArticleSort, SortDirection
from app.models import Article


def get_articles(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    source: str | None = None,
    sort: ArticleSort = ArticleSort.published_at,
    direction: SortDirection = SortDirection.desc,
):
    query = db.query(Article)

    if source:
        query = query.filter(Article.source == source)

    sort_columns = {
        ArticleSort.published_at: Article.published_at,
        ArticleSort.headline: Article.headline,
        ArticleSort.loaded_at: Article.loaded_at,
    }

    order_by = sort_columns[sort]

    if direction == SortDirection.asc:
        query = query.order_by(order_by.asc())
    else:
        query = query.order_by(order_by.desc())

    total = query.count()

    articles = (
        query
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "items": articles,
    }


def get_article(
    db: Session,
    article_id: int,
):
    return (
        db.query(Article)
        .filter(Article.id == article_id)
        .first()
    )