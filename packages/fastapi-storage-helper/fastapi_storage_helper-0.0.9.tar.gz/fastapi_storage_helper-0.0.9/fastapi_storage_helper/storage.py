import boto3
from boto.s3.connection import S3Connection
from botocore.config import Config
from botocore.exceptions import NoCredentialsError


class StorageService:
    def __init__(
        self, access_key_id: str, secret_key: str, region_name: str, bucket: str
    ):
        self.bucket = bucket
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_key,
            region_name=region_name,
            config=Config(signature_version="v4"),
        )
        self.s3_v2 = S3Connection(
            aws_access_key_id=access_key_id, aws_secret_access_key=secret_key
        )

    def create_upload_presign_url(
        self,
        key: str,
        content_length: int,
        content_type: str,
        media_id: str,
        user_id: str,
    ):
        return self.s3.generate_presigned_post(
            self.bucket,
            key,
            Conditions=[
                {"Content-Type": content_type},
                {"x-amz-meta-id": media_id},
                {"x-amz-meta-user_id": user_id},
                ["content-length-range", 0, content_length],
            ],
            Fields={
                "x-amz-meta-id": media_id,
                "x-amz-meta-user_id": user_id,
                "Content-Type": content_type,
                "bucket": self.bucket,
            },
            ExpiresIn=1 * 60 * 60,
        )

    # Use boto2 to resolve performance issue
    def create_read_presign_url(self, key: str):
        return self.s3_v2.generate_url(
            7 * 24 * 60 * 60, "GET", bucket=self.bucket, key=key, query_auth=True
        )

    def create_read_nerver_expired_presign_url(self, key: str):
        expiration = 1 * 365 * 7 * 24 * 60 * 60
        return self.s3_v2.generate_url(
            expiration, "GET", bucket=self.bucket, key=key, query_auth=True
        )

    def get_metadata(self, path: str):
        return self.s3.head_object(Bucket=self.bucket, Key=path).get("Metadata")

    def upload_file_to_s3(self, file_path: str, s3_path: str):
        try:
            self.s3.upload_file(file_path, self.bucket, s3_path)
            print("Upload Successful")
            return True
        except FileNotFoundError:
            print("The file was not found")
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False

    def change_content_type(self, key, content_type: str = "image/jpeg"):
        copy_source = {"Bucket": self.bucket, "Key": key}
        metadata = self.s3.head_object(Bucket=self.bucket, Key=key)["Metadata"]

        self.s3.copy_object(
            CopySource=copy_source,
            Bucket=self.bucket,
            Key=key,
            MetadataDirective="REPLACE",
            ContentType=content_type,
            Metadata=metadata,
        )
