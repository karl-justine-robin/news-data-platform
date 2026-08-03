from fastapi import FastAPI

from api.app.routers import (
    analytics,
    articles,
    health,
    pipeline,
    search,
)

from api.app.exceptions import register_exception_handlers

app = FastAPI(
    title="News Data Platform API",
    description="""
A production-style REST API for the News Data Platform.

Features:

- Browse articles
- Search articles
- Analytics endpoints
- Pipeline execution
- Pipeline monitoring

Built with:

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
)
def root():
    return {
        "message": "News Data Platform API is running"
    }