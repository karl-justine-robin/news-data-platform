from http import HTTPStatus

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from api.app import crud, schemas
from api.app.constants import API_PREFIX
from api.app.database import get_db
from api.app.enums import ArticleSort, SortDirection


router = APIRouter(
    prefix=f"{API_PREFIX}/search",
    tags=["Search"],
)


@router.get(
    "",
    status_code=HTTPStatus.OK,
    response_model=schemas.ArticleList,
    summary="Search articles",
    description=(
        "Searches news articles by keyword. "
        "Supports pagination and sorting of the search results."
    ),
    response_description="Paginated list of matching articles.",
    operation_id="search_articles",
    responses={
        HTTPStatus.OK: {
            "description": "Search completed successfully.",
        },
        HTTPStatus.BAD_REQUEST: {
            "description": "Invalid search query or request parameters.",
        },
    },
)
def search_articles(
    q: str = Query(
        ...,
        min_length=1,
        description="Keyword to search for.",
        example="economy",
    ),
    page: int = Query(
        default=1,
        ge=1,
        description="Page number (starts at 1).",
        example=1,
    ),
    size: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Number of articles per page.",
        example=10,
    ),
    sort: ArticleSort = Query(
        default=ArticleSort.published_at,
        description="Field used to sort the results.",
        example=ArticleSort.published_at,
    ),
    direction: SortDirection = Query(
        default=SortDirection.desc,
        description="Sort direction.",
        example=SortDirection.desc,
    ),
    db: Session = Depends(get_db),
) -> schemas.ArticleList:

    skip = (page - 1) * size

    result = crud.search_articles(
        db=db,
        q=q,
        skip=skip,
        limit=size,
        sort=sort,
        direction=direction,
    )

    return schemas.ArticleList(
        page=page,
        size=size,
        total=result["total"],
        items=result["items"],
    )