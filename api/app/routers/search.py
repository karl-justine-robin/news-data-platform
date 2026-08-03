from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from api.app import crud, schemas
from api.app.database import get_db
from api.app.enums import ArticleSort, SortDirection

from api.app.constants import API_PREFIX

router = APIRouter(
    prefix=f"{API_PREFIX}/search",
    tags=["Search"],
)


@router.get(
    "",
    response_model=schemas.ArticleList,
    summary="Search articles",
    description="Searches news articles by keyword with support for pagination and sorting.",
    response_description="Paginated list of matching articles",
    responses={
        400: {
            "description": "Invalid search query",
        },
    },
)
def search_articles(
    q: str = Query(
        ...,
        min_length=1,
        description="Keyword to search for",
    ),
    page: int = Query(
        1,
        ge=1,
        description="Page number",
    ),
    size: int = Query(
        10,
        ge=1,
        le=100,
        description="Number of articles per page",
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

    result = crud.search_articles(
        db=db,
        q=q,
        skip=skip,
        limit=size,
        sort=sort,
        direction=direction,
    )

    return {
        "page": page,
        "size": size,
        "total": result["total"],
        "items": result["items"],
    }