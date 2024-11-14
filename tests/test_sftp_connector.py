from unittest import TestCase
from unittest.mock import Mock

from paramiko.ssh_exception import SSHException, AuthenticationException

from sftp_file_navigator import SFTPConnector
from utils.specified_exceptions import FailedSFTPSessionConnectionError, SFTPAuthenticationError

host = "some_host"
username = "cool_username"
password = "secret_password"
specific_port = 13
default_port = 22


class TestSFTPConnector(TestCase):
    def setUp(self) -> None:
        self.mock_client = Mock()
        self.connector = SFTPConnector(self.mock_client)

    def test_set_sftp_session__makes_expected_request_to_connect_session(self):
        self.connector.set_sftp_session(host, username, password, specific_port)
        self.mock_client.connect.assert_called_once_with(**{
            "hostname": host, "username": username, "password": password, "port": specific_port
        })

    def test_set_sftp_session__no_port_specified__sets_default_port_value(self):
        self.connector.set_sftp_session(host, username, password)
        self.mock_client.connect.assert_called_once_with(**{
            "hostname": host, "username": username, "password": password, "port": default_port
        })

    def test_close_sftp_session__makes_expected_requests_to_close_session(self):
        self.connector.set_sftp_session(host, username, password)
        self.connector.close_sftp_session()

        self.mock_client.close.assert_called_once()
        self.mock_client.open_sftp.return_value.close.assert_called_once()  # mock_session

    def test_set_sftp_session__session_connection_failed__raises_expected_error(self):
        with self.assertRaises(FailedSFTPSessionConnectionError):
            self.mock_client.open_sftp.side_effect = SSHException()
            self.connector.set_sftp_session(host, username, password, default_port)

    def test_set_sftp_session__authentication_failed__raises_expected_error(self):
        with self.assertRaises(SFTPAuthenticationError):
            self.mock_client.connect.side_effect = AuthenticationException()
            self.connector.set_sftp_session(host, username, password, default_port)
