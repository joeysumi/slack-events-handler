from config import GALLERY_PATH, ACCEPTABLE_FILE_FORMATS
from sftp_connection import SFTPNavigator
from slack_api import SlackApiRequester
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

    SUCCESSFUL_CHALLENGE_MESSAGE = "A valid challenge received."
    FAILED_CHALLENGE_MESSAGE = "Did not receive a valid challenge."

    def __init__(
            self,
            slack_bot_token,
            sftp_host,
            sftp_username,
            sftp_password,
            sftp_port,
            api_requester=SlackApiRequester,
            sftp_navigator=SFTPNavigator,
            **kwargs
    ) -> None:
        self._sftp_host = sftp_host
        self._sftp_username = sftp_username
        self._sftp_password = sftp_password
        self._sftp_port = sftp_port
        self._sftp_navigator = sftp_navigator  # lazy loads
        self._sftp = None

        self.api_requester = api_requester(bot_token=slack_bot_token)

    @property
    def sftp(self):
        if self._sftp is None:
            self._sftp = self._sftp_navigator(
                self._sftp_host,
                self._sftp_username,
                self._sftp_password,
                self._sftp_port
            )
        return self._sftp

    @classmethod
    def respond_to_url_verification(cls, response: dict) -> dict:
        """ Response to Slack Events API url verification. """
        token = response.get("token")
        challenge = response.get("challenge")
        data = {}

        if token and challenge:
            data["status"] = "success"
            data["challenge"] = challenge
            data["message"] = cls.SUCCESSFUL_CHALLENGE_MESSAGE
        else:
            data["status"] = "failed"
            data["message"] = cls.FAILED_CHALLENGE_MESSAGE

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

        file_url = file_data["file"]["thumb_1024"]
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
            file_format = self._get_file_format(file_name)
            raise FileFormatError(f"{Err.FILE_FORMAT_ERROR}: Format is {file_format}")

        if not self._is_file_from_expected_channel(file_channel_id, file_data["file"]["channels"]):
            raise WrongChannelProvidedError(Err.WRONG_CHANNEL_ERROR)

    def _is_valid_file_type(self, file_name: str) -> bool:
        file_type = self._get_file_format(file_name)
        return file_type.lower() in ACCEPTABLE_FILE_FORMATS

    @staticmethod
    def _get_file_format(file_name: str) -> str:
        return file_name[file_name.rfind(".") + 1:]  # one removes the '.' from the file format

    @staticmethod
    def _is_file_from_expected_channel(expected_channel: str, source_channels: list) -> bool:
        return expected_channel in source_channels

    def _save_image_to_sftp_file(self, image_data, image_name, channel_name):
        try:
            directory_path = f"{GALLERY_PATH}/{channel_name}"
            if self.sftp.is_file_in_directory(directory_path, image_name):
                raise FileAlreadyExistsError(Err.FILE_EXISTS)

            self.sftp.save_file_to_directory(image_data, f"{directory_path}/{image_name}")

        except Exception as err:
            print(f"An SFTP Error occurred: {err}")
