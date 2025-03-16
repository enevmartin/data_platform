# apps/core/storage/s3.py
from apps.core.storage.base import StorageInterface
import boto3
from django.conf import settings


class S3Storage(StorageInterface):
    def __init__(self):
        s3_config = settings.STORAGE_OPTIONS.get('s3', {})
        self.bucket = s3_config.get('BUCKET')
        self.client = boto3.client(
            's3',
            aws_access_key_id=s3_config.get('ACCESS_KEY'),
            aws_secret_access_key=s3_config.get('SECRET_KEY'),
            region_name=s3_config.get('REGION')
        )

    def save(self, file_obj, file_path):
        try:
            self.client.upload_fileobj(file_obj, self.bucket, file_path)
            return f"s3://{self.bucket}/{file_path}"
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error saving to S3: {str(e)}")
            raise