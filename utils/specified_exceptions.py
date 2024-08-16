class ErrorMessages:
    WRONG_EVENT_TYPE = "The event type cannot be handled."
    EVENT_HANDLED_SUCCESSFULLY = "File event handled successfully."
    FILE_EXISTS = "File already exists at the specified directory."
    FILE_FORMAT_ERROR = "Cannot accept file format."
    SLACK_RETRIEVAL_ERROR = "There was an error retrieving the file from Slack API."
    WRONG_CHANNEL_ERROR = "File was not found in expected channels."


class UnexpectedEventTypeError(Exception):
    pass


class FileAlreadyExistsError(Exception):
    pass


class FileFormatError(Exception):
    pass


class SlackApiError(Exception):
    pass


class WrongChannelProvidedError(Exception):
    pass


class FailedSFTPSessionConnectionError(Exception):
    pass


class SFTPAuthenticationError(Exception):
    pass


class SFTPTimeoutError(Exception):
    pass
