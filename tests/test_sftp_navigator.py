from unittest import TestCase
from unittest.mock import MagicMock

from sftp_file_navigator import SFTPNavigator

fake_file = "Fake File"
correct_directory = "directory/to/file"
wrong_directory = "wrong/directory/to/file"
directory_path_does_not_exist = "wrong/directory/raise/error"


def create_file_directory_response(directory):
    if directory == correct_directory:
        return ["File One", "File Two", fake_file]
    elif directory == wrong_directory:
        return ["File One", "File Two"]
    elif directory == directory_path_does_not_exist:
        raise FileNotFoundError
    else:
        raise NotImplementedError


class TestSFTPNavigator(TestCase):
    def setUp(self) -> None:
        self.mocked_connector = MagicMock(**{
            "sftp_session.listdir.side_effect": create_file_directory_response
        })
        self.navigator = SFTPNavigator(
            host="some_host",
            username="some_user",
            password="my_secret_password",
            port=1,
            sftp_connector=self.mocked_connector,
        )

    def test_is_file_in_directory__file_exists_in_directory__returns_true(self):
        actual = self.navigator.is_file_in_directory(correct_directory, fake_file)
        self.assertTrue(actual)

    def test_is_file_in_directory__file_does_not_exist_in_directory__returns_false(self):
        actual = self.navigator.is_file_in_directory(correct_directory, "Wrong File")
        self.assertFalse(actual)

    def test_is_file_in_directory__directory_does_not_exist__returns_false(self):
        actual = self.navigator.is_file_in_directory(wrong_directory, fake_file)
        self.assertFalse(actual)

    def test_is_file_in_directory__directory_does_not_exist__handles_error(self):
        """ Error should not be raised """
        self.navigator.is_file_in_directory(directory_path_does_not_exist, fake_file)

    def test_is_file_in_directory__directory_does_not_exist__creates_a_new_directory(self):
        self.navigator.is_file_in_directory(directory_path_does_not_exist, fake_file)
        self.mocked_connector.sftp_session.mkdir.assert_called_once_with(directory_path_does_not_exist)

    def test_is_file_in_directory__file_does_not_exist__does_not_create_a_new_directory(self):
        self.navigator.is_file_in_directory(wrong_directory, fake_file)
        self.mocked_connector.sftp_session.mkdir.assert_not_called()

    def test_save_file_to_directory__makes_expected_request_to_save_file(self):
        self.navigator.save_file_to_directory(b'Some data', correct_directory)
        self.mocked_connector.sftp_session.open.assert_called_once_with(correct_directory, "wb+")
