from typing import Dict

import requests


class APIClientError(Exception):
    pass


class APIClient:
    def __init__(self, address: str):
        self.address = address

    def post(self, body: Dict, api_key: str, app_id: str):
        headers = {
            "Content-Type": "application/json",
            "Zenetics-api-key": api_key,
        }

        response = requests.post(
            self.address + f"/api/v1/apps/{app_id}/sessions", json=body, headers=headers
        )
        if response.status_code != 200:
            raise APIClientError(
                f"Failed to post to {self.address}. Status code {response.status_code}"
            )
