from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


# =====================================================
# Articles
# =====================================================

class Article(BaseModel):
    id: int
    headline: str
    published_at: date
    body: str
    source: str
    loaded_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class ArticleList(BaseModel):
    page: int
    size: int
    total: int
    items: list[Article]


# =====================================================
# Health
# =====================================================

class HealthResponse(BaseModel):
    status: str
    database: str
    version: str
    pipeline: str
    timestamp: datetime

# =====================================================
# Analytics
# =====================================================

class SourceAnalytics(BaseModel):
    source: str
    count: int


class PublicationTrend(BaseModel):
    published_at: date
    count: int

class WarehouseSourceAnalytics(BaseModel):
    source: str
    article_count: int


class WarehouseDateAnalytics(BaseModel):
    date: date
    article_count: int


class WarehouseMonthAnalytics(BaseModel):
    year: int
    month: int
    month_name: str
    article_count: int


class WarehouseDayAnalytics(BaseModel):
    day_of_week: str
    article_count: int


# =====================================================
# Pipeline
# =====================================================

class PipelineRun(BaseModel):
    id: int
    pipeline_name: str
    status: str

    start_time: datetime
    end_time: datetime | None

    duration_seconds: float
    records_processed: int

    error_message: str | None

    model_config = ConfigDict(
        from_attributes=True
    )


class PipelineStats(BaseModel):
    total_runs: int
    successful_runs: int
    failed_runs: int
    success_rate: float
    average_duration_seconds: float
    total_records_processed: int


class PipelineRunResponse(BaseModel):
    message: str
    run: PipelineRun


# =====================================================
# Errors
# =====================================================

class ErrorResponse(BaseModel):
    success: bool = False
    status_code: int
    message: str


# =====================================================
# Quality
# =====================================================

class QualityMetricsResponse(BaseModel):
    total_records: int
    valid_records: int
    invalid_records: int

    missing_headline: int
    missing_body: int
    missing_source: int
    invalid_date: int

    quality_score: float