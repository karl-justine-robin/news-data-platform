from http import HTTPStatus

from fastapi import APIRouter

from api.app import schemas
from api.app.constants import API_PREFIX


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
        "Checks whether the News Data Platform API is "
        "running and able to accept requests."
    ),
    response_description="API health status.",
    operation_id="health_check",
    responses={
        HTTPStatus.OK: {
            "description": "API is healthy.",
        },
    },
)
def health() -> schemas.HealthResponse:
    return schemas.HealthResponse(
        status="healthy",
    )