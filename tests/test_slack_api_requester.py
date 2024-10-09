from unittest import TestCase
from unittest.mock import Mock

from slack_api.slack_api_requester import SlackApiRequester

channel = "my-channel"
fake_file_info = {
    "ok": True,
    "file": {
        "id": "file_id",
        "name": "file_name",
        "url_private": "https://slack_url.com/this/is/an/image",
        "shares": {
            "public": {
                channel: [{
                    "channel_name": channel,
                }]
            }
        },
        "channels": [
            channel,
        ]
    }
}


class TestSlackApiRequester(TestCase):

    FILE_DATA = fake_file_info
    IMAGE_DATA = b"image"

    def setUp(self) -> None:
        self.bot_token = "some_token"
        self.request_service = Mock(**{
            "get.return_value.json.return_value": self.FILE_DATA,
            "get.return_value.content": self.IMAGE_DATA,
        })
        self.api_requester = SlackApiRequester(self.bot_token, self.request_service)

    def test_get_file_data__request_header_authorization_initialized_as_expected(self):
        actual_auth = self.api_requester.request_headers.get("Authorization")
        expected_auth = f"Bearer {self.bot_token}"
        self.assertEqual(expected_auth, actual_auth)

    def test_get_file_data__file_id_given__returns_expected_data(self):
        file_id = "some_id"
        actual_data = self.api_requester.get_file_data(file_id)
        self.assertEqual(self.FILE_DATA, actual_data)

    def test_get_image_data__file_url_given__returns_expected_data(self):
        file_url = "https://some_url.com"
        actual_data = self.api_requester.get_image_data(file_url)
        self.assertEqual(self.IMAGE_DATA, actual_data)
