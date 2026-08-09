from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.app import crud, schemas
from api.app.constants import API_PREFIX
from api.app.database import get_db

from src.framework.analytics.analytics_service import (
    AnalyticsService,
)


router = APIRouter(
    prefix=f"{API_PREFIX}/analytics",
    tags=["Analytics"],
)

analytics_service = AnalyticsService()


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


@router.get(
    "/warehouse/sources",
    status_code=HTTPStatus.OK,
    response_model=list[
        schemas.WarehouseSourceAnalytics
    ],
    summary="Get warehouse article counts by source",
    description=(
        "Returns article counts grouped by source "
        "from the warehouse fact table."
    ),
    operation_id="get_warehouse_articles_by_source",
)
def get_warehouse_sources():

    results = (
        analytics_service
        .articles_by_source()
    )

    return [
        {
            "source": result.source,
            "article_count": result.article_count,
        }
        for result in results
    ]


@router.get(
    "/warehouse/dates",
    status_code=HTTPStatus.OK,
    response_model=list[
        schemas.WarehouseDateAnalytics
    ],
    summary="Get warehouse article counts by date",
    description=(
        "Returns article counts grouped by publication "
        "date from the warehouse."
    ),
    operation_id="get_warehouse_articles_by_date",
)
def get_warehouse_dates():

    results = (
        analytics_service
        .articles_by_date()
    )

    return [
        {
            "date": result.date,
            "article_count": result.article_count,
        }
        for result in results
    ]


@router.get(
    "/warehouse/months",
    status_code=HTTPStatus.OK,
    response_model=list[
        schemas.WarehouseMonthAnalytics
    ],
    summary="Get warehouse article counts by month",
    description=(
        "Returns article counts grouped by year and "
        "month from the warehouse."
    ),
    operation_id="get_warehouse_articles_by_month",
)
def get_warehouse_months():

    results = (
        analytics_service
        .articles_by_month()
    )

    return [
        {
            "year": result.year,
            "month": result.month,
            "month_name": result.month_name,
            "article_count": result.article_count,
        }
        for result in results
    ]


@router.get(
    "/warehouse/days-of-week",
    status_code=HTTPStatus.OK,
    response_model=list[
        schemas.WarehouseDayAnalytics
    ],
    summary="Get warehouse article counts by day of week",
    description=(
        "Returns article counts grouped by day of week "
        "from the warehouse."
    ),
    operation_id="get_warehouse_articles_by_day_of_week",
)
def get_warehouse_days_of_week():

    results = (
        analytics_service
        .articles_by_day_of_week()
    )

    return [
        {
            "day_of_week": result.day_of_week,
            "article_count": result.article_count,
        }
        for result in results
    ]