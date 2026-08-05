from datetime import date, datetime

from pydantic import BaseModel


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

    class Config:
        from_attributes = True


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

    class Config:
        from_attributes = True


class PipelineStats(BaseModel):
    total_runs: int
    successful_runs: int
    failed_runs: int
    success_rate: float


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