from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.app import crud
from api.app.database import get_db

from pathlib import Path
import sys

# Allow the API project to import the ETL framework
ROOT_DIR = Path(__file__).resolve().parents[3]
sys.path.append(str(ROOT_DIR))

from src.framework.pipeline import Pipeline

router = APIRouter(
    prefix="/pipeline",
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


@router.post("/run")
def run_pipeline():

    pipeline = Pipeline()

    pipeline.run()

    return {
        "status": "SUCCESS",
        "message": "Pipeline executed successfully."
    }