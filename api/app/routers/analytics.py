from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.app import crud
from api.app.database import get_db

from api.app.constants import API_PREFIX

router = APIRouter(
    prefix=f"{API_PREFIX}/analytics",
    tags=["Analytics"],
)

@router.get(
    "/sources",
    summary="Get article counts by source",
    description="Returns the total number of articles grouped by news source.",
    response_description="List of article counts by source",
)
def get_sources(
    db: Session = Depends(get_db),
):
    return crud.get_articles_by_source(db)


@router.get(
    "/publication-trend",
    summary="Get publication trend",
    description="Returns the number of published articles grouped by publication date.",
    response_description="Publication trend",
)
def get_publication_trend(
    db: Session = Depends(get_db),
):
    return crud.get_publication_trend(db)