from fastapi.testclient import TestClient

from api.app.main import app


client = TestClient(app)


def test_get_latest_quality():

    response = client.get(
        "/api/v1/quality/latest"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_records"] >= 0
    assert data["valid_records"] >= 0
    assert data["invalid_records"] >= 0

    assert "missing_headline" in data
    assert "missing_body" in data
    assert "missing_source" in data
    assert "invalid_date" in data

    assert "quality_score" in data


def test_quality_score_is_valid():

    response = client.get(
        "/api/v1/quality/latest"
    )

    assert response.status_code == 200

    data = response.json()

    assert 0 <= data["quality_score"] <= 100