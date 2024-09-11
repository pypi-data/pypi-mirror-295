import boto3

from tenyks_sdk.file_providers.aws.data_classes import AWSS3Credentials
from tenyks_sdk.file_providers.aws.s3_client import S3Client


class Boto3S3ClientFactory:
    @staticmethod
    def create_client(aws_s3_credentials: AWSS3Credentials) -> S3Client:
        session = boto3.Session(
            aws_access_key_id=aws_s3_credentials.aws_access_key_id,
            aws_secret_access_key=aws_s3_credentials.aws_secret_access_key,
            region_name=aws_s3_credentials.region_name,
        )

        return S3Client(session.client("s3"))
