from fastapi.testclient import TestClient

from api.app.main import app


client = TestClient(app)


def test_pipeline_stats():

    response = client.get(
        "/api/v1/pipeline/stats"
    )

    assert response.status_code == 200

    data = response.json()

    assert "total_runs" in data
    assert "successful_runs" in data
    assert "failed_runs" in data
    assert "success_rate" in data
    assert "average_duration_seconds" in data
    assert "total_records_processed" in data


def test_latest_pipeline_run():

    response = client.get(
        "/api/v1/pipeline/runs/latest"
    )

    assert response.status_code == 200

    data = response.json()

    assert "id" in data
    assert "pipeline_name" in data
    assert "status" in data
    assert "start_time" in data
    assert "duration_seconds" in data
    assert "records_processed" in data


def test_pipeline_runs():

    response = client.get(
        "/api/v1/pipeline/runs"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    for run in data:
        assert "id" in run
        assert "pipeline_name" in run
        assert "status" in run
        assert "start_time" in run
        assert "duration_seconds" in run
        assert "records_processed" in run


def test_pipeline_failed_run():

    response = client.get(
        "/api/v1/pipeline/runs"
    )

    assert response.status_code == 200

    data = response.json()

    failed_runs = [
        run
        for run in data
        if run["status"] == "FAILED"
    ]

    if failed_runs:

        run = failed_runs[0]

        assert run["error_message"] is not None
        assert run["records_processed"] >= 0
        assert run["duration_seconds"] >= 0