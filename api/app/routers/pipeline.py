from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.app import crud
from api.app.database import get_db

from api.app.response_models import SuccessResponse

from src.framework.pipeline import Pipeline

from api.app.constants import API_PREFIX


router = APIRouter(
    prefix=f"{API_PREFIX}/pipeline",
    tags=["Pipeline"],
)


@router.get("/runs")
def get_pipeline_runs(
    db: Session = Depends(get_db),
):
    return crud.get_pipeline_runs(db)


@router.get("/runs/latest")
def get_latest_pipeline_run(
    db: Session = Depends(get_db),
):
    return crud.get_latest_pipeline_run(db)


@router.get("/stats")
def get_pipeline_stats(
    db: Session = Depends(get_db),
):
    return crud.get_pipeline_stats(db)


@router.post(
    "/run",
    response_model=SuccessResponse,
    summary="Run ETL Pipeline",
    description="Triggers the ETL pipeline manually.",
    responses={
        500: {
            "description": "Pipeline execution failed",
        },
    },
)
def run_pipeline():

    pipeline = Pipeline()
    pipeline.run()

    return SuccessResponse(
        message="Pipeline executed successfully."
    )