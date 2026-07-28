from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(
    prefix="/articles",
    tags=["Articles"],
)


@router.get("", response_model=list[schemas.Article])
def get_articles(db: Session = Depends(get_db)):
    return crud.get_articles(db)


@router.get("/{article_id}", response_model=schemas.Article)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = crud.get_article(db, article_id)

    if article is None:
        raise HTTPException(
            status_code=404,
            detail="Article not found",
        )

    return article