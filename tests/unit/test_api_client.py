from unittest.mock import Mock, patch

from dashboard.api_client import APIClient
from requests import HTTPError


API_URL = "http://127.0.0.1:8000"


def test_get_articles():

    client = APIClient(API_URL)

    mock_response = Mock()
    mock_response.json.return_value = {
        "items": [
            {
                "id": 1,
                "headline": "Test article",
            }
        ]
    }

    mock_response.raise_for_status.return_value = None

    with patch(
        "dashboard.api_client.requests.get",
        return_value=mock_response,
    ) as mock_get:

        result = client.get_articles(
            {"page": 1}
        )

    assert result["items"][0]["id"] == 1

    mock_get.assert_called_once_with(
        f"{API_URL}/api/v1/articles",
        params={"page": 1},
        timeout=10,
    )


def test_search_articles():

    client = APIClient(API_URL)

    mock_response = Mock()
    mock_response.json.return_value = {
        "items": []
    }

    mock_response.raise_for_status.return_value = None

    with patch(
        "dashboard.api_client.requests.get",
        return_value=mock_response,
    ) as mock_get:

        result = client.search_articles(
            "bitcoin"
        )

    assert result["items"] == []

    mock_get.assert_called_once_with(
        f"{API_URL}/api/v1/search",
        params={"q": "bitcoin"},
        timeout=10,
    )


def test_get_warehouse_sources():

    client = APIClient(API_URL)

    mock_response = Mock()
    mock_response.json.return_value = [
        {
            "source": "Reuters",
            "article_count": 10,
        }
    ]

    mock_response.raise_for_status.return_value = None

    with patch(
        "dashboard.api_client.requests.get",
        return_value=mock_response,
    ) as mock_get:

        result = client.get_warehouse_sources()

    assert result[0]["source"] == "Reuters"

    mock_get.assert_called_once_with(
        f"{API_URL}/api/v1/analytics/warehouse/sources",
        timeout=10,
    )


def test_get_warehouse_dates():

    client = APIClient(API_URL)

    mock_response = Mock()
    mock_response.json.return_value = []

    mock_response.raise_for_status.return_value = None

    with patch(
        "dashboard.api_client.requests.get",
        return_value=mock_response,
    ) as mock_get:

        result = client.get_warehouse_dates()

    assert result == []

    mock_get.assert_called_once_with(
        f"{API_URL}/api/v1/analytics/warehouse/dates",
        timeout=10,
    )


def test_get_warehouse_months():

    client = APIClient(API_URL)

    mock_response = Mock()
    mock_response.json.return_value = []

    mock_response.raise_for_status.return_value = None

    with patch(
        "dashboard.api_client.requests.get",
        return_value=mock_response,
    ) as mock_get:

        result = client.get_warehouse_months()

    assert result == []

    mock_get.assert_called_once_with(
        f"{API_URL}/api/v1/analytics/warehouse/months",
        timeout=10,
    )


def test_get_warehouse_days_of_week():

    client = APIClient(API_URL)

    mock_response = Mock()
    mock_response.json.return_value = []

    mock_response.raise_for_status.return_value = None

    with patch(
        "dashboard.api_client.requests.get",
        return_value=mock_response,
    ) as mock_get:

        result = client.get_warehouse_days_of_week()

    assert result == []

    mock_get.assert_called_once_with(
        f"{API_URL}/api/v1/analytics/warehouse/days-of-week",
        timeout=10,
    )


def test_get_warehouse_sources_raises_http_error():

    client = APIClient(
        "http://127.0.0.1:8000"
    )

    mock_response = Mock()

    mock_response.raise_for_status.side_effect = (
        HTTPError("500 Server Error")
    )

    with patch(
        "dashboard.api_client.requests.get",
        return_value=mock_response,
    ):

        try:

            client.get_warehouse_sources()

            assert False, (
                "Expected HTTPError to be raised"
            )

        except HTTPError as error:

            assert str(error) == (
                "500 Server Error"
            )


def test_get_pipeline_runs():

    client = APIClient(
        "http://127.0.0.1:8000"
    )

    mock_response = Mock()

    mock_response.json.return_value = [
        {
            "id": 1,
            "pipeline_name": "news_pipeline",
            "status": "SUCCESS",
            "records_processed": 30,
        }
    ]

    mock_response.raise_for_status.return_value = None

    with patch(
        "dashboard.api_client.requests.get",
        return_value=mock_response,
    ) as mock_get:

        result = client.get_pipeline_runs()

    assert result[0]["id"] == 1
    assert result[0]["status"] == "SUCCESS"

    mock_get.assert_called_once_with(
        "http://127.0.0.1:8000/api/v1/pipeline/runs",
        timeout=10,
    )