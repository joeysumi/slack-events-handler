from datetime import datetime as dt

from sftp_connection import SFTPConnector


def log(text):
    """ Required for Google CLoud Console Logging. The 'print' function logs."""
    print(text)


class SFTPNavigator:

    GALLERY_PATH = "./public_html/wp-content/gallery"
    DEFAULT_CUTOFF_TIME_IN_SECONDS = 60 * 60 * 24 * 365

    def __init__(self, host=None, username=None, password=None, port=None, sftp_connector=SFTPConnector()):
        self._host = host
        self._username = username
        self._password = password
        self._port = port
        self._connector = sftp_connector
        self._sftp_session = None

    @property
    def sftp_session(self):
        if self._sftp_session is None:
            self._connector.set_sftp_session(
                host=self._host,
                username=self._username,
                password=self._password,
                port=self._port,
            )
            self._sftp_session = self._connector.sftp_session
        return self._sftp_session

    def _create_file(self, path: str) -> None:
        self.sftp_session.mkdir(path)
        log(f"File '{path}' created.")

    def is_file_in_directory(self, directory_path: str, file_name: str) -> bool:
        """ Checks to see if file exists in directory

        Returns:
            True if file exists
            False if file does not exist in an existing path, creating path if necessary
        """
        try:
            directory_contents = self.sftp_session.listdir(directory_path)
            return file_name in directory_contents
        except FileNotFoundError:  # no file/directory found
            self._create_file(directory_path)
            return False

    def save_file_to_directory(self, file_data: bytes, file_path: str):
        with self.sftp_session.open(file_path, "wb+") as file:
            file.write(file_data)
