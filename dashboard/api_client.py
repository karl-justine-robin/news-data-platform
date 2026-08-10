import requests


class APIClient:

    def __init__(
        self,
        base_url,
        timeout=10,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get_articles(
        self,
        params=None,
    ):

        response = requests.get(
            f"{self.base_url}/api/v1/articles",
            params=params,
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()

    def search_articles(
        self,
        query,
    ):

        response = requests.get(
            f"{self.base_url}/api/v1/search",
            params={
                "q": query,
            },
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()

    def get_warehouse_sources(self):

        response = requests.get(
            f"{self.base_url}/api/v1/analytics/warehouse/sources",
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()

    def get_warehouse_dates(self):

        response = requests.get(
            f"{self.base_url}/api/v1/analytics/warehouse/dates",
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()

    def get_warehouse_months(self):

        response = requests.get(
            f"{self.base_url}/api/v1/analytics/warehouse/months",
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()

    def get_warehouse_days_of_week(self):

        response = requests.get(
            f"{self.base_url}/api/v1/analytics/warehouse/days-of-week",
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()



    def get_pipeline_stats(self):

        response = requests.get(
            f"{self.base_url}/api/v1/pipeline/stats",
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()


    def get_latest_pipeline_run(self):

        response = requests.get(
            f"{self.base_url}/api/v1/pipeline/runs/latest",
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()


    def get_pipeline_runs(self):

        response = requests.get(
            f"{self.base_url}/api/v1/pipeline/runs",
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()



    def get_latest_quality(self):

        response = requests.get(
            f"{self.base_url}/api/v1/quality/latest",
            timeout=self.timeout,
        )

        response.raise_for_status()

        return response.json()