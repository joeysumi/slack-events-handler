from sftp_connector import SFTPConnector


def log(text):
    """ Required for Google CLoud Console Logging. The 'print' function logs."""
    print(text)


class SFTPNavigator:

    GALLERY_PATH = "./public_html/wp-content/gallery"

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

    def _create_file(self, file_name: str, default_path=True) -> None:
        file_path = f"{self.GALLERY_PATH}/{file_name}" if default_path is True else file_name
        self.sftp_session.mkdir(file_path)
        log(f"File '{file_name}' created.")

    def is_file_in_directory(self, directory_path: str, file_name: str) -> bool:
        directory_contents = self.sftp_session.listdir(directory_path)
        return file_name in directory_contents

    def save_file_to_directory(self, file_data: bytes, file_path: str):
        with self.sftp_session.open(file_path, "wb+") as file:
            file.write(file_data)
