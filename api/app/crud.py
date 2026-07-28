from sqlalchemy.orm import Session

from app.models import Article


def get_articles(db: Session):
    return (
        db.query(Article)
        .order_by(Article.published_at.desc())
        .all()
    )


def get_article(db: Session, article_id: int):
    return (
        db.query(Article)
        .filter(Article.id == article_id)
        .first()
    )