from urllib.parse import urljoin
import uuid

import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import NoCredentialsError

from django.conf import settings

from pokemon.models import FileUpload


class UploadToS3:

    @classmethod
    def get_s3_client(cls):
        return boto3.client(
            service_name="s3",
            aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

    @classmethod
    def upload_to_s3(cls, file_object, name):
        filename = '.'.join([str(uuid.uuid4()), name.split(".")[-1]])
        s3_client = cls.get_s3_client()
        try:
            s3_client.upload_fileobj(file_object, settings.AWS_STORAGE_BUCKET_NAME, filename)
            return True, urljoin(settings.AWS_S3_URL, filename)
        except ClientError as e:
            return False, f'{e.__class__} {e}'

    @classmethod
    def upload_file(cls, label, user_id, file_object, name):
        status, url = cls.upload_to_s3(file_object=file_object, name=name)
        if status:
            file_upload = FileUpload.objects.create(file_label=label, file_url=url, user_id=user_id)
            return True, file_upload, "Created Successfully"
        return False, None, f"Error in file upload {url}"

    @classmethod
    def upload_file_from_path(cls, file_path, name):
        s3_client = cls.get_s3_client()
        try:
            filename = '.'.join([str(uuid.uuid4()), name.split(".")[-1]])
            s3_client.upload_file(file_path, settings.AWS_STORAGE_BUCKET_NAME, filename)
            return True, urljoin(settings.AWS_S3_URL, filename)
        except ClientError as e:
            return False, f'{e.__class__} {e}'
        except FileNotFoundError:
            return False, "The file was not found"
        except NoCredentialsError:
            return False, "Credentials not available"

