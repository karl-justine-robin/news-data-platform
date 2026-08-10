from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.app.exceptions import register_exception_handlers
from api.app.logger import logger
from api.app.routers import (
    analytics,
    articles,
    health,
    pipeline,
    quality,
    search,
)

from api.app.middleware.request_logger import (
    RequestLoggingMiddleware,
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("API started.")

    yield

    logger.info("API stopped.")


openapi_tags = [
    {
    "name": "Quality",
    "description": "Data quality metrics and validation results.",
    },
    {
        "name": "Health",
        "description": "Health check endpoints for monitoring API availability.",
    },
    {
        "name": "Articles",
        "description": "Browse, filter, and retrieve news articles.",
    },
    {
        "name": "Search",
        "description": "Search news articles using keywords.",
    },
    {
        "name": "Analytics",
        "description": "Article statistics and publication analytics.",
    },
    {
        "name": "Pipeline",
        "description": "Execute and monitor the ETL pipeline.",
    },
    {
        "name": "Root",
        "description": "General API information.",
    },
]

app = FastAPI(
    title="News Data Platform API",
    description="""
A production-style REST API for the News Data Platform.

## Features

- Browse news articles
- Search articles
- Article analytics
- Execute ETL pipelines
- Monitor pipeline runs

## Technology Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Python ETL Framework
""",
    version="1.0.0",
    contact={
        "name": "Karl Justine Robin",
    },
    license_info={
        "name": "MIT",
    },
    openapi_tags=openapi_tags,
    lifespan=lifespan,
)

register_exception_handlers(app)

app.include_router(health.router)
app.include_router(articles.router)
app.include_router(search.router)
app.include_router(analytics.router)
app.include_router(pipeline.router)
app.include_router(quality.router)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8501",
        "http://127.0.0.1:8501",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    GZipMiddleware,
    minimum_size=1000,
)




@app.get(
    "/",
    tags=["Root"],
    summary="API Root",
    description="Returns a welcome message indicating that the API is running.",
)
def root() -> dict[str, str]:
    return {
        "message": "News Data Platform API is running",
    }