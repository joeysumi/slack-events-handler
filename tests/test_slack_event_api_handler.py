from unittest import TestCase
from unittest.mock import Mock

from slack_event_api_handler import SlackEventApiHandler
from utils.specified_exceptions import UnexpectedEventTypeError, SlackApiError, FileFormatError, \
    WrongChannelProvidedError

file_id = "12345"
channel_id = "6789"
channel_name = "general"
image_url = "https://private_url_to_image.com"
image_name = "image.jpg"
fake_file_data = {
    "file": {
        "name": image_name,
        "channels": [channel_id],
        "shares": {
            "public": {
                channel_id: [{
                    "channel_name": channel_name,
                }]
            }
        },
        "url_private": image_url,
    }
}
fake_file_data_no_event = {"color": "blue"}
fake_file_data_wrong_format = {"file": {"name": "myfile.mov"}}
fake_file_data_wrong_channels = {"file": {"name": image_name, "channels": ['0', '1']}}
fake_event_data_wrong_event_type = {"event": {"type": "wrong_type"}}
fake_event_data = {
    "event": {
        "type": "file_shared",
        "file_id": file_id,
        "channel_id": channel_id,
    }
}
image_data = b"this_is_the_image_data"


def create_fake_challenge_response(token=None, challenge=None) -> dict:
    if not token and not challenge:
        return {}
    return {"token": token, "challenge": challenge}


class TestSlackEventApiHandler(TestCase):

    def setUp(self) -> None:
        self._fake_file_data = None  # will be lazy loaded for exception tests
        self.mock_requester = Mock(**{
            "return_value.get_image_data.return_value": image_data
        })
        self.mock_navigator = Mock(**{
            "return_value.is_file_in_directory.return_value": False
        })
        self.api_handler = SlackEventApiHandler(
            api_requester=self.mock_requester,
            sftp_navigator=self.mock_navigator,
        )
        self.token = "some_token"
        self.challenge = "some_challenge"

    @property
    def fake_file_data(self):
        return self._fake_file_data

    @fake_file_data.setter
    def fake_file_data(self, value):
        self._fake_file_data = value
        self.mock_requester.return_value.get_file_data.return_value = self._fake_file_data

    def test_respond_to_url_verification__token_and_challenge_given__returns_success_message(self):
        actual = self.api_handler.respond_to_url_verification(
            {"token": self.token, "challenge": self.challenge}
        )
        expected = {
            "challenge": self.challenge,
            "message": self.api_handler.SUCCESSFUL_CHALLENGE_MESSAGE,
            "status": "success",
        }
        self.assertEqual(expected, actual)

    def test_respond_to_url_verification__token_and_challenge_missing__returns_failed_message(self):
        actual = self.api_handler.respond_to_url_verification({"no_challenge_dict": "No Token"})
        expected = {
            "message": self.api_handler.FAILED_CHALLENGE_MESSAGE,
            "status": "failed",
        }
        self.assertEqual(expected, actual)

    def test_handle_slack_event__file_shared_event__makes_expected_file_request_to_slack(self):
        self.fake_file_data = fake_file_data
        self.api_handler.handle_slack_event(fake_event_data)

        self.mock_requester.return_value.get_file_data.assert_called_once_with(file_id)

    def test_handle_slack_event__file_shared_event__makes_expected_image_request_to_slack(self):
        self.fake_file_data = fake_file_data
        self.api_handler.handle_slack_event(fake_event_data)

        self.mock_requester.return_value.get_image_data.assert_called_once_with(image_url)

    def test_handle_slack_event__file_shared_event__makes_expected_request_to_sftp(self):
        self.fake_file_data = fake_file_data
        self.api_handler.handle_slack_event(fake_event_data)

        expected_request = image_data, f"{self.api_handler.SFTP_DEFAULT_GALLERY_PATH}/{channel_name}/{image_name}"

        self.mock_navigator.return_value.save_file_to_directory.assert_called_once_with(*expected_request)

    # Test Exceptions ----------------------------------------

    def test_handle_slack_event__the_wrong_event_type__raises_expected_exception(self):
        with self.assertRaises(UnexpectedEventTypeError):
            self.api_handler.handle_slack_event(fake_event_data_wrong_event_type)

    def test_handle_slack_event__file_data_does_not_include_file__raises_expected_exception(self):
        with self.assertRaises(SlackApiError):
            self.fake_file_data = fake_file_data_no_event
            self.api_handler.handle_slack_event(fake_event_data)

    def test_handle_slack_event__file_is_an_unacceptable_format__raises_expected_exception(self):
        with self.assertRaises(FileFormatError):
            self.fake_file_data = fake_file_data_wrong_format
            self.api_handler.handle_slack_event(fake_event_data)

    def test_handle_slack_event__file_is_not_in_an_expected_channel__raises_expected_exception(self):
        with self.assertRaises(WrongChannelProvidedError):
            self.fake_file_data = fake_file_data_wrong_channels
            self.api_handler.handle_slack_event(fake_event_data)
