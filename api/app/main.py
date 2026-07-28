from fastapi import FastAPI

from app.routers import articles, health

app = FastAPI(
    title="News Data Platform API",
    version="1.0.0",
)

app.include_router(health.router)
app.include_router(articles.router)


@app.get("/")
def root():
    return {
        "message": "News Data Platform API is running"
    }