import boto3

from file_navigator import FileNavigatorBase


class S3Navigator(FileNavigatorBase):

    def __init__(self, bucket_name, **kwargs):
        self._s3_resource = None
        self._s3_bucket = None
        self.bucket_name = bucket_name

    @property
    def s3_resource(self):
        if self._s3_resource is None:
            self._s3_resource = boto3.resource("s3")
        return self._s3_resource

    @property
    def s3_bucket(self):
        if self._s3_bucket is None:
            self._s3_bucket = self.s3_resource.Bucket(self.bucket_name)
        return self._s3_bucket

    def is_file_in_directory(self, directory_path: str, file_name: str) -> bool:
        """ Checks to see if file exists in directory (s3 uses "key")

        Returns:
            True if file exists
            False if file does not exist in an existing path, creating path if necessary
        """
        bucket_collection = self.s3_bucket.objects.filter(Prefix=directory_path)
        object_name_list = [obj.key for obj in bucket_collection]
        for name in object_name_list:
            if file_name in name:
                return True
        return False

    def save_file_to_directory(self, file_data: bytes, file_path: str):
        """ Saves the file to the S3 Bucket, if the path doesn't exist, it will create one
            Thus it is important to have the correct path or there will be variations and different "folders"
        """
        img_obj = self.s3_resource.Object(self.bucket_name, file_path)
        img_obj.put(Body=file_data)
