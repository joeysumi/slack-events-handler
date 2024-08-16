import os

from sftp_connection import SFTPNavigator
from slack_api_requester import SlackApiRequester
from utils.specified_exceptions import (
    ErrorMessages as Err,
    UnexpectedEventTypeError,
    SlackApiError,
    FileFormatError,
    WrongChannelProvidedError,
    FileAlreadyExistsError
)


def return_status(status, message):
    return {
        "status": status,
        "message": message,
    }


class SlackEventApiHandler:

    ACCEPTABLE_FILE_FORMATS = [
        "jpeg",
        "jpg",
        "png",
    ]

    SFTP_DEFAULT_GALLERY_PATH = "public_html/wp-content/gallery"
    SUCCESSFUL_CHALLENGE_MESSAGE = "A valid challenge received."
    FAILED_CHALLENGE_MESSAGE = "Did not receive a valid challenge."

    def __init__(
            self,
            api_requester=SlackApiRequester,
            sftp_navigator=SFTPNavigator,
    ) -> None:
        self._host = os.environ.get("SFTP_HOST")
        self._username = os.environ.get("SFTP_USERNAME")
        self._password = os.environ.get("SFTP_PASSWORD")
        self._port = os.environ.get("SFTP_PORT", 22)
        self._sftp_navigator = sftp_navigator

        self.api_requester = api_requester()
        self.wp_url = os.environ.get("WP_WEBHOOK_URL", "")

    def respond_to_url_verification(self, response: dict) -> dict:
        """ Response to Slack Events API url verification. """
        token = response.get("token")
        challenge = response.get("challenge")
        data = {}

        if token and challenge:
            data["status"] = "success"
            data["challenge"] = challenge
            data["message"] = self.SUCCESSFUL_CHALLENGE_MESSAGE
        else:
            data["status"] = "failed"
            data["message"] = self.FAILED_CHALLENGE_MESSAGE

        return data

    def handle_slack_event(self, event_data: dict) -> None:
        """ When a Slack event arrives, determines how the event is to be handled by event type. """
        if event_data["event"]["type"] != "file_shared":
            raise UnexpectedEventTypeError(Err.WRONG_EVENT_TYPE)

        self._handle_new_file_event(event_data)

    def _handle_new_file_event(self, file_event_data: dict) -> None:
        """ When a file creation event is received from Slack, this method responds to slack to obtain the file data,
            the image data and downloads the image to the correct SFTP location.
        """
        file_id = file_event_data["event"]["file_id"]
        file_channel_id = file_event_data["event"]["channel_id"]

        file_data = self._get_file_data_from_slack(file_id, file_channel_id)

        file_name = file_data["file"]["name"]
        channel_name = file_data["file"]["shares"]["public"][file_channel_id][0]["channel_name"]

        file_url = file_data["file"]["url_private"]
        image = self.api_requester.get_image_data(file_url)

        self._save_image_to_sftp_file(image, file_name, channel_name)

    def _get_file_data_from_slack(self, file_id: str, file_channel_id: str) -> dict:
        file_data = self.api_requester.get_file_data(file_id)
        self._verify_file_data(file_data, file_channel_id)

        return file_data

    def _verify_file_data(self, file_data, file_channel_id):
        if not file_data.get("file"):
            raise SlackApiError(Err.SLACK_RETRIEVAL_ERROR)

        file_name = file_data["file"]["name"]
        if not self._is_valid_file_type(file_name):
            raise FileFormatError(Err.FILE_FORMAT_ERROR)

        if not self._is_file_from_expected_channel(file_channel_id, file_data["file"]["channels"]):
            raise WrongChannelProvidedError(Err.WRONG_CHANNEL_ERROR)

    def _is_valid_file_type(self, file_name: str) -> bool:
        file_type = file_name[file_name.rfind(".") + 1:]  # one removes the '.' from the file format
        return file_type.lower() in self.ACCEPTABLE_FILE_FORMATS

    @staticmethod
    def _is_file_from_expected_channel(expected_channel: str, source_channels: list) -> bool:
        return expected_channel in source_channels

    def _save_image_to_sftp_file(self, image_data, image_name, channel_name):
        try:
            sftp = self._sftp_navigator(self._host, self._username, self._password, self._port)
            # directory_path = f"{self.SFTP_DEFAULT_GALLERY_PATH}/{channel_name}"
            directory_path = f"{self.SFTP_DEFAULT_GALLERY_PATH}/test_folder"
            if sftp.is_file_in_directory(directory_path, image_name):
                raise FileAlreadyExistsError(Err.FILE_EXISTS)

            sftp.save_file_to_directory(image_data, f"{directory_path}/{image_name}")

        except Exception as err:
            print(f"An SFTP Error occurred: {err}")
