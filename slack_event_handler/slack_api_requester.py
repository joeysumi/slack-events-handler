import os

import requests


class SlackApiRequester:
    SLACK_API_BASE_URL = "https://slack.com/api"
    FILE_INFO_ENDPOINT = "files.info"
    CHAT_INFO_ENDPOINT = "conversations.info"

    def __init__(self, requester=requests) -> None:
        self._bot_token = os.environ.get("SLACK_BOT_TOKEN", "some_token")
        self.request_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._bot_token}",
        }
        self.requester = requester

    def get_api_token(self):
        return self._bot_token

    def _make_request(self, method, url, jsonify, **kwargs):
        if method == "GET":
            response = self.requester.get(url, headers=self.request_headers, **kwargs)
            response.raise_for_status()

            if jsonify is True:
                return response.json()
            return response

    def get_file_data(self, file_id: str) -> dict:
        file_response = self._make_request(
            "GET",
            f"{self.SLACK_API_BASE_URL}/{self.FILE_INFO_ENDPOINT}",
            params={"file": file_id},
            jsonify=True,
        )
        return file_response

    def get_image_data(self, file_url):
        image_response = self._make_request("GET", file_url, jsonify=False)
        return image_response.content
