from unittest import TestCase
from unittest.mock import patch, Mock

from s3_connection import S3Navigator

fake_image_name = "some_image.jpg"
mocked_response = {
    "resource.return_value.Bucket.return_value.objects.filter.return_value": [
        Mock(**{"key": "gallery/"}),
        Mock(**{"key": f"gallery/{fake_image_name}"}),
    ],
}


class TestS3Navigator(TestCase):

    def setUp(self) -> None:
        self.patched_boto = patch("s3_connection.s3_navigator.boto3", **mocked_response)
        self.fake_boto3 = self.patched_boto.start()
        self.navigator = S3Navigator(bucket_name="my_bucket")

    def tearDown(self) -> None:
        self.patched_boto.stop()

    def test_is_file_in_directory__file_exists_in_directory__returns_true(self):
        actual = self.navigator.is_file_in_directory("gallery/", fake_image_name)
        self.assertTrue(actual)

    def test_is_file_in_directory__file_does_not_exist__returns_false(self):
        actual = self.navigator.is_file_in_directory("gallery/", "another_image.jpg")
        self.assertFalse(actual)

    def test_save_file_to_directory__makes_expected_request_to_save_the_file(self):
        file_bytes = b"this is a file"
        file_path = "the/path/to/the/file.mp4"
        self.navigator.save_file_to_directory(file_bytes, file_path)
        self.fake_boto3.resource.return_value.Object.assert_called_once_with(self.navigator.bucket_name, file_path)
        self.fake_boto3.resource.return_value.Object.return_value.put.assert_called_once_with(Body=file_bytes)
        pass
