from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("/sources")
def get_sources(db: Session = Depends(get_db)):
    return crud.get_articles_by_source(db)

@router.get("/publication-trend")
def get_publication_trend(db: Session = Depends(get_db)):
    return crud.get_publication_trend(db)