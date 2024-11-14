from config import SOURCE_CONNECTION
from file_navigator.s3_file_navigator import S3Navigator
from file_navigator.sftp_file_navigator import SFTPNavigator
from slack_api import SlackEventApiHandler, SlackApiRequester


class EventHandlerFactory:
    """ Factory that instantiates the handler class with the correct connection destination """

    CONNECTION_MAP = {
        "s3": S3Navigator,
        "sftp": SFTPNavigator,
    }

    def create(self, **credentials):
        """ Creates and instantiates the handler
            Determines which type of connection as stated in the Config module
        """
        storage_navigator_class = self.CONNECTION_MAP[SOURCE_CONNECTION]
        storage_navigator = storage_navigator_class(**credentials)
        slack_api_requester = SlackApiRequester(bot_token=credentials["bot_token"])

        handler = SlackEventApiHandler(
            file_storage_navigator=storage_navigator,
            slack_api_requester=slack_api_requester,
        )
        return handler
