import requests


class NestOpsClient:
    def __init__(self, api_key):
        if api_key is None:
            raise ValueError("Api key must not be none")
        self.api_key = api_key

    def get_request(self, endpoint, params):
        url = f"https://nestops-dashboard.cloud.flyzipline.com/{endpoint}"
        headers = {"X-Api-Key": self.api_key}
        response = requests.get(url, timeout=20, headers=headers, params=params)
        response.raise_for_status()
        return response

    def get_snapshot(self, nest_code, start, end):
        # TODO start and end times
        response = self.get_request(
            "api/snapshot", {"nest": nest_code, "start": start, "end": end}
        )

        return response.json()
