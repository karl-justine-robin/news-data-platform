from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from api.app import crud, schemas
from api.app.database import get_db
from api.app.enums import ArticleSort, SortDirection

router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


@router.get("", response_model=schemas.ArticleList)
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
        description="Sort field",
    ),
    direction: SortDirection = Query(
        SortDirection.desc,
        description="Sort direction",
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