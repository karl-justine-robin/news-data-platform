from dataclasses import dataclass
from datetime import date


@dataclass
class SourceArticleCount:
    source: str
    article_count: int


@dataclass
class DateArticleCount:
    date: date
    article_count: int


@dataclass
class MonthArticleCount:
    year: int
    month: int
    month_name: str
    article_count: int


@dataclass
class DayOfWeekArticleCount:
    day_of_week: str
    article_count: int