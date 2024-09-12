import base64
import boto3
from botocore.exceptions import ClientError


class S3Linker:
    def __init__(self, bucket, region_name="us-east-1"):
        self.bucket = bucket
        self.region_name = region_name
        self.s3 = boto3.client("s3", region_name=self.region_name)

    def upload_file(self, file_path, object_name=None):
        """Upload a file to an S3 bucket

        :param file_path: File to upload
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        if object_name is None:
            object_name = file_path

        try:
            self.s3.upload_file(file_path, self.bucket, object_name)
        except ClientError as e:
            print(f"Error uploading file: {e}")
            return False
        return True

    def download_file(self, object_name, file_path):
        """Download a file from an S3 bucket

        :param object_name: S3 object name to download
        :param file_path: Local path to save the file
        :return: True if file was downloaded, else False
        """
        try:
            self.s3.download_file(self.bucket, object_name, file_path)
        except ClientError as e:
            print(f"Error downloading file: {e}")
            return False
        return True

    def list_objects(self, prefix=""):
        """List objects in the S3 bucket

        :param prefix: Only fetch objects whose key starts with this prefix
        :return: List of object keys
        """
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=prefix)
            return [obj["Key"] for obj in response.get("Contents", [])]
        except ClientError as e:
            print(f"Error listing objects: {e}")
            return []

    def delete_object(self, object_name):
        """Delete an object from the S3 bucket

        :param object_name: S3 object name to delete
        :return: True if object was deleted, else False
        """
        try:
            self.s3.delete_object(Bucket=self.bucket, Key=object_name)
            return True
        except ClientError as e:
            print(f"Error deleting object: {e}")
            return False

    def get_presigned_url(self, object_name, expiration=3600):
        """Generate a presigned URL for the S3 object

        :param object_name: S3 object name
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """
        try:
            response = self.s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": object_name},
                ExpiresIn=expiration,
            )
        except ClientError as e:
            print(f"Error generating presigned URL: {e}")
            return None
        return response

    def get_image_base64(self, object_name):
        """Get an image from S3 and return it as a base64 encoded string

        :param object_name: S3 object name
        :return: Base64 encoded string of the image. If error, returns None.
        """
        try:
            response = self.s3.get_object(Bucket=self.bucket, Key=object_name)
            image_content = response["Body"].read()
            base64_encoded = base64.b64encode(image_content).decode("utf-8")
            return base64_encoded
        except ClientError as e:
            print(f"Error retrieving image: {e}")
            return None

    def list_images(
        self, prefix="", allowed_extensions=(".jpg", ".jpeg", ".png", ".gif")
    ):
        """List image objects in the S3 bucket

        :param prefix: Only fetch objects whose key starts with this prefix
        :param allowed_extensions: Tuple of allowed file extensions
        :return: List of image object keys
        """
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=prefix)
            return [
                obj["Key"]
                for obj in response.get("Contents", [])
                if obj["Key"].lower().endswith(allowed_extensions)
            ]
        except ClientError as e:
            print(f"Error listing images: {e}")
            return []
