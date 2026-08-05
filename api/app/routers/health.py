from datetime import datetime
from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from api.app import schemas
from api.app.constants import API_PREFIX
from api.app.database import get_db


router = APIRouter(
    prefix=f"{API_PREFIX}/health",
    tags=["Health"],
)


@router.get(
    "",
    status_code=HTTPStatus.OK,
    response_model=schemas.HealthResponse,
    summary="Health check",
    description=(
        "Checks the health of the News Data Platform API "
        "and verifies database connectivity."
    ),
    response_description="API health status.",
    operation_id="health_check",
    responses={
        HTTPStatus.OK: {
            "description": "API is healthy.",
        },
    },
)
def health(
    db: Session = Depends(get_db),
) -> schemas.HealthResponse:

    database_status = "disconnected"

    try:
        db.execute(text("SELECT 1"))
        database_status = "connected"

    except Exception:
        database_status = "disconnected"

    return schemas.HealthResponse(
        status="healthy",
        database=database_status,
        version="1.0.0",
        pipeline="ready",
        timestamp=datetime.utcnow(),
    )