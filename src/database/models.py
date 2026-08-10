from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)

from src.database.database import Base


class Article(Base):
    __tablename__ = "articles"

    __table_args__ = (
        UniqueConstraint(
            "headline",
            "published_at",
            "source",
            name="uq_articles_headline_date_source",
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    headline = Column(
        Text,
        nullable=False,
    )

    published_at = Column(
        Date,
        nullable=False,
    )

    body = Column(
        Text,
        nullable=False,
    )

    source = Column(
        String(100),
        nullable=False,
    )

    loaded_at = Column(
        DateTime,
        nullable=False,
    )


class PipelineRun(Base):
    __tablename__ = "pipeline_runs"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    pipeline_name = Column(
        String(100),
    )

    status = Column(
        String(50),
    )

    start_time = Column(
        DateTime,
    )

    end_time = Column(
        DateTime,
    )

    duration_seconds = Column(
        Float,
    )

    records_processed = Column(
        Integer,
    )

    error_message = Column(
        Text,
    )


class DimDate(Base):
    __tablename__ = "dim_date"

    date_key = Column(
        Integer,
        primary_key=True,
    )

    full_date = Column(
        Date,
        nullable=False,
        unique=True,
    )

    year = Column(
        Integer,
        nullable=False,
    )

    month = Column(
        Integer,
        nullable=False,
    )

    month_name = Column(
        String(20),
        nullable=False,
    )

    day = Column(
        Integer,
        nullable=False,
    )

    day_of_week = Column(
        String(20),
        nullable=False,
    )


class DimSource(Base):
    __tablename__ = "dim_source"

    source_key = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    source_name = Column(
        String(100),
        nullable=False,
        unique=True,
    )


class DimCategory(Base):
    __tablename__ = "dim_category"

    category_key = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    category_name = Column(
        String(100),
        nullable=False,
        unique=True,
    )


class FactArticle(Base):
    __tablename__ = "fact_article"

    __table_args__ = (
        UniqueConstraint(
            "headline",
            "published_at",
            "source_key",
            name="uq_fact_article_headline_date_source",
        ),
    )

    article_key = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    date_key = Column(
        Integer,
        ForeignKey("dim_date.date_key"),
        nullable=False,
    )

    source_key = Column(
        Integer,
        ForeignKey("dim_source.source_key"),
        nullable=False,
    )

    category_key = Column(
        Integer,
        ForeignKey("dim_category.category_key"),
        nullable=True,
    )

    headline = Column(
        Text,
        nullable=False,
    )

    published_at = Column(
        DateTime,
        nullable=False,
    )

    loaded_at = Column(
        DateTime,
        nullable=False,
    )


class QualityRun(Base):
    __tablename__ = "quality_runs"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    total_records = Column(
        Integer,
        nullable=False,
    )

    valid_records = Column(
        Integer,
        nullable=False,
    )

    invalid_records = Column(
        Integer,
        nullable=False,
    )

    missing_headline = Column(
        Integer,
        nullable=False,
    )

    missing_body = Column(
        Integer,
        nullable=False,
    )

    missing_source = Column(
        Integer,
        nullable=False,
    )

    invalid_date = Column(
        Integer,
        nullable=False,
    )

    quality_score = Column(
        Float,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        nullable=False,
    )