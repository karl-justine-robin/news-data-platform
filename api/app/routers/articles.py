from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from api.app import crud, schemas
from api.app.database import get_db
from api.app.enums import ArticleSort, SortDirection

from api.app.constants import API_PREFIX

router = APIRouter(
    prefix=f"{API_PREFIX}/articles",
    tags=["Articles"],
)

@router.get(
    "",
    response_model=schemas.ArticleList,
    summary="List articles",
    description="Returns a paginated list of news articles. Supports filtering by source, sorting, and pagination.",
    response_description="Paginated list of articles",
    responses={
        400: {
            "description": "Invalid request parameters",
        },
    },
)
def get_articles(
    page: int = Query(
        1,
        ge=1,
        description="Page number (starts at 1)",
    ),
    size: int = Query(
        10,
        ge=1,
        le=100,
        description="Number of articles per page",
    ),
    source: str | None = Query(
        None,
        description="Filter articles by source",
    ),
    sort: ArticleSort = Query(
        ArticleSort.published_at,
        description="Field used to sort the results",
    ),
    direction: SortDirection = Query(
        SortDirection.desc,
        description="Sort direction (ascending or descending)",
    ),
    db: Session = Depends(get_db),
):
    skip = (page - 1) * size

    result = crud.get_articles(
        db=db,
        skip=skip,
        limit=size,
        source=source,
        sort=sort,
        direction=direction,
    )

    return {
        "page": page,
        "size": size,
        "total": result["total"],
        "items": result["items"],
    }


@router.get(
    "/{article_id}",
    response_model=schemas.Article,
    summary="Get article",
    description="Returns a single news article by its unique ID.",
    response_description="Article details",
    responses={
        404: {
            "description": "Article not found",
        },
    },
)
def get_article(
    article_id: int,
    db: Session = Depends(get_db),
):
    article = crud.get_article(
        db,
        article_id,
    )

    if article is None:
        raise HTTPException(
            status_code=404,
            detail="Article not found",
        )

    return article