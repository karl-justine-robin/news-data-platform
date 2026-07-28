from enum import Enum


class ArticleSort(str, Enum):
    published_at = "published_at"
    headline = "headline"
    loaded_at = "loaded_at"


class SortDirection(str, Enum):
    asc = "asc"
    desc = "desc"