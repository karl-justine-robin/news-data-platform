from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from api.app import models
from api.app.enums import ArticleSort, SortDirection
from api.app.models import Article

def get_publication_trend(db):
    results = (
        db.query(
            models.Article.published_at,
            func.count(models.Article.id).label("count"),
        )
        .group_by(models.Article.published_at)
        .order_by(models.Article.published_at)
        .all()
    )

    return [
        {
            "published_at": row.published_at,
            "count": row.count,
        }
        for row in results
    ]

def get_articles_by_source(db):
    results = (
        db.query(
            models.Article.source,
            func.count(models.Article.id).label("count"),
        )
        .group_by(models.Article.source)
        .order_by(func.count(models.Article.id).desc())
        .all()
    )

    return [
        {
            "source": row.source,
            "count": row.count,
        }
        for row in results
    ]

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



def search_articles(
    db: Session,
    q: str,
    skip: int = 0,
    limit: int = 10,
    sort: ArticleSort = ArticleSort.published_at,
    direction: SortDirection = SortDirection.desc,
):
    query = (
        db.query(Article)
        .filter(
            or_(
                Article.headline.ilike(f"%{q}%"),
                Article.body.ilike(f"%{q}%"),
            )
        )
    )

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