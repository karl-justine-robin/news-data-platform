from sqlalchemy import func

from src.database.database import SessionLocal
from src.database.models import (
    DimDate,
    DimSource,
    FactArticle,
)

from src.framework.analytics.analytics_models import (
    DateArticleCount,
    DayOfWeekArticleCount,
    MonthArticleCount,
    SourceArticleCount,
)


class AnalyticsService:

    def articles_by_source(self):

        db = SessionLocal()

        try:

            results = (
                db.query(
                    DimSource.source_name,
                    func.count(
                        FactArticle.article_key
                    ).label("article_count"),
                )
                .join(
                    FactArticle,
                    FactArticle.source_key
                    == DimSource.source_key,
                )
                .group_by(
                    DimSource.source_name
                )
                .order_by(
                    func.count(
                        FactArticle.article_key
                    ).desc()
                )
                .all()
            )

            return [
                SourceArticleCount(
                    source=source_name,
                    article_count=article_count,
                )
                for source_name, article_count
                in results
            ]

        finally:

            db.close()

    def articles_by_date(self):

        db = SessionLocal()

        try:

            results = (
                db.query(
                    DimDate.full_date,
                    func.count(
                        FactArticle.article_key
                    ).label("article_count"),
                )
                .join(
                    FactArticle,
                    FactArticle.date_key
                    == DimDate.date_key,
                )
                .group_by(
                    DimDate.full_date
                )
                .order_by(
                    DimDate.full_date
                )
                .all()
            )

            return [
                DateArticleCount(
                    date=full_date,
                    article_count=article_count,
                )
                for full_date, article_count
                in results
            ]

        finally:

            db.close()

    def articles_by_month(self):

        db = SessionLocal()

        try:

            results = (
                db.query(
                    DimDate.year,
                    DimDate.month,
                    DimDate.month_name,
                    func.count(
                        FactArticle.article_key
                    ).label("article_count"),
                )
                .join(
                    FactArticle,
                    FactArticle.date_key
                    == DimDate.date_key,
                )
                .group_by(
                    DimDate.year,
                    DimDate.month,
                    DimDate.month_name,
                )
                .order_by(
                    DimDate.year,
                    DimDate.month,
                )
                .all()
            )

            return [
                MonthArticleCount(
                    year=year,
                    month=month,
                    month_name=month_name,
                    article_count=article_count,
                )
                for (
                    year,
                    month,
                    month_name,
                    article_count,
                ) in results
            ]

        finally:

            db.close()

    def articles_by_day_of_week(self):

        db = SessionLocal()

        try:

            results = (
                db.query(
                    DimDate.day_of_week,
                    func.count(
                        FactArticle.article_key
                    ).label("article_count"),
                )
                .join(
                    FactArticle,
                    FactArticle.date_key
                    == DimDate.date_key,
                )
                .group_by(
                    DimDate.day_of_week
                )
                .order_by(
                    DimDate.day_of_week
                )
                .all()
            )

            return [
                DayOfWeekArticleCount(
                    day_of_week=day_of_week,
                    article_count=article_count,
                )
                for (
                    day_of_week,
                    article_count,
                ) in results
            ]

        finally:

            db.close()


    def summary(self):

        return {
            "articles_by_source": self.articles_by_source(),
            "articles_by_date": self.articles_by_date(),
            "articles_by_month": self.articles_by_month(),
            "articles_by_day_of_week": (
                self.articles_by_day_of_week()
            ),
        }