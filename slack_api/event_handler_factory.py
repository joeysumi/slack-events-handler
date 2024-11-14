from config import SOURCE_CONNECTION
from s3_connection import S3Navigator
from sftp_connection import SFTPNavigator
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
        navigator_class = self.CONNECTION_MAP[SOURCE_CONNECTION]
        navigator = navigator_class(**credentials)
        slack_api_requester = SlackApiRequester(bot_token=credentials["bot_token"])

        handler = SlackEventApiHandler(navigator=navigator, api_requester=slack_api_requester)
        return handler