from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.app import crud, schemas
from api.app.constants import API_PREFIX
from api.app.database import get_db

router = APIRouter(
    prefix=f"{API_PREFIX}/analytics",
    tags=["Analytics"],
)


@router.get(
    "/sources",
    status_code=HTTPStatus.OK,
    response_model=list[schemas.SourceAnalytics],
    summary="Get article counts by source",
    description=(
        "Returns the total number of articles grouped "
        "by news source."
    ),
    response_description="List of article counts grouped by source.",
    operation_id="get_articles_by_source",
    responses={
        HTTPStatus.OK: {
            "description": "Article counts retrieved successfully.",
        },
    },
)
def get_sources(
    db: Session = Depends(get_db),
) -> list[schemas.SourceAnalytics]:
    return crud.get_articles_by_source(db)


@router.get(
    "/publication-trend",
    status_code=HTTPStatus.OK,
    response_model=list[schemas.PublicationTrend],
    summary="Get publication trend",
    description=(
        "Returns the number of published articles "
        "grouped by publication date."
    ),
    response_description="Publication trend by date.",
    operation_id="get_publication_trend",
    responses={
        HTTPStatus.OK: {
            "description": "Publication trend retrieved successfully.",
        },
    },
)
def get_publication_trend(
    db: Session = Depends(get_db),
) -> list[schemas.PublicationTrend]:
    return crud.get_publication_trend(db)