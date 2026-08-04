from fastapi import FastAPI

from api.app.exceptions import register_exception_handlers
from api.app.routers import (
    analytics,
    articles,
    health,
    pipeline,
    search,
)

openapi_tags = [
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
)

register_exception_handlers(app)

app.include_router(health.router)
app.include_router(articles.router)
app.include_router(search.router)
app.include_router(analytics.router)
app.include_router(pipeline.router)


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