from datetime import date, datetime

from pydantic import BaseModel


class Article(BaseModel):
    id: int
    headline: str
    published_at: date
    body: str
    source: str
    loaded_at: datetime

    model_config = {
        "from_attributes": True
    }


class ArticleList(BaseModel):
    page: int
    size: int
    total: int
    items: list[Article]