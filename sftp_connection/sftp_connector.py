import paramiko
from paramiko.ssh_exception import AuthenticationException, SSHException

from utils.specified_exceptions import FailedSFTPSessionConnectionError, SFTPAuthenticationError


class SFTPConnector:

    def __init__(self, ssh_client=paramiko.SSHClient()):
        self._ssh_client = ssh_client
        self._sftp_session = None

    @property
    def sftp_session(self):
        return self._sftp_session

    def _connect_to_sftp(self, host=None, username=None, password=None, port=None):
        try:
            self._ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self._ssh_client.connect(hostname=host, port=port, username=username, password=password)
            print("Connected to SFTP server.")
        except AuthenticationException as error:
            raise SFTPAuthenticationError(f"Authentication Failed: {error}")
        except TimeoutError as error:
            print(f"Connection Timedout: {error}")

    def set_sftp_session(self, host, username, password, port=22):
        self._connect_to_sftp(host=host, username=username, password=password, port=port)
        try:
            self._sftp_session = self._ssh_client.open_sftp()
        except SSHException as error:
            raise FailedSFTPSessionConnectionError(f"Failed to open a SFTP session SSH session is not active: {error}")

    def close_sftp_session(self):
        self._sftp_session.close()
        self._ssh_client.close()
        print("Closed SFTP session and disconnected from SFTP server.")
