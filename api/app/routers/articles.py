from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from api.app import crud, schemas
from api.app.database import get_db
from api.app.enums import ArticleSort, SortDirection

router = APIRouter(
    prefix="/articles",
    tags=["Articles"],
)


@router.get("", response_model=schemas.ArticleList)
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
        description="Field to sort by",
    ),
    direction: SortDirection = Query(
        SortDirection.desc,
        description="Sort direction",
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


@router.get("/{article_id}", response_model=schemas.Article)
def get_article(
    article_id: int,
    db: Session = Depends(get_db),
):
    article = crud.get_article(db, article_id)

    if article is None:
        raise HTTPException(
            status_code=404,
            detail="Article not found",
        )

    return article