from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.app import crud, schemas
from api.app.constants import API_PREFIX
from api.app.database import get_db

from src.framework.pipeline import Pipeline


router = APIRouter(
    prefix=f"{API_PREFIX}/pipeline",
    tags=["Pipeline"],
)


@router.get(
    "/runs",
    status_code=HTTPStatus.OK,
    response_model=list[schemas.PipelineRun],
    summary="List pipeline runs",
    description="Returns the execution history of the ETL pipeline.",
    response_description="Pipeline execution history.",
    operation_id="list_pipeline_runs",
    responses={
        HTTPStatus.OK: {
            "description": "Pipeline runs retrieved successfully.",
        },
    },
)
def get_pipeline_runs(
    db: Session = Depends(get_db),
) -> list[schemas.PipelineRun]:

    return crud.get_pipeline_runs(db)


@router.get(
    "/runs/latest",
    status_code=HTTPStatus.OK,
    response_model=schemas.PipelineRun,
    summary="Get latest pipeline run",
    description="Returns the most recent ETL pipeline execution.",
    response_description="Latest pipeline run.",
    operation_id="get_latest_pipeline_run",
    responses={
        HTTPStatus.OK: {
            "description": "Latest pipeline run retrieved successfully.",
        },
    },
)
def get_latest_pipeline_run(
    db: Session = Depends(get_db),
) -> schemas.PipelineRun:

    return crud.get_latest_pipeline_run(db)


@router.get(
    "/stats",
    status_code=HTTPStatus.OK,
    response_model=schemas.PipelineStats,
    summary="Get pipeline statistics",
    description=(
        "Returns summary statistics for all ETL pipeline executions."
    ),
    response_description="Pipeline statistics.",
    operation_id="get_pipeline_statistics",
    responses={
        HTTPStatus.OK: {
            "description": "Pipeline statistics retrieved successfully.",
        },
    },
)
def get_pipeline_stats(
    db: Session = Depends(get_db),
) -> schemas.PipelineStats:

    return crud.get_pipeline_stats(db)


@router.post(
    "/run",
    status_code=HTTPStatus.OK,
    response_model=schemas.PipelineRunResponse,
    summary="Run ETL pipeline",
    description="Triggers the ETL pipeline manually.",
    response_description="Pipeline execution result.",
    operation_id="run_pipeline",
    responses={
        HTTPStatus.OK: {
            "description": "Pipeline executed successfully.",
        },
        HTTPStatus.INTERNAL_SERVER_ERROR: {
            "description": "Pipeline execution failed.",
        },
    },
)
def run_pipeline(
    db: Session = Depends(get_db),
) -> schemas.PipelineRunResponse:

    pipeline = Pipeline()
    pipeline.run()

    latest_run = crud.get_latest_pipeline_run(db)

    return schemas.PipelineRunResponse(
        message="Pipeline executed successfully.",
        run=latest_run,
    )