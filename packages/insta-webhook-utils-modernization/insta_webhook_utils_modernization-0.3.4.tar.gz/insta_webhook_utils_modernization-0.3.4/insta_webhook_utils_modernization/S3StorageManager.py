import re
from urllib.parse import parse_qs, urlparse

import boto3
import requests
from botocore.exceptions import BotoCoreError, ClientError


class S3StorageManager:

    def __init__(self, access_key, secret_key, environ, region='ap-south-1'):
        self.s3_client = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key,
                                      region_name=region)
        self.environ = environ

    def upload_file(self, file_content_or_url, bucket, file_name):
        try:
            # If it's a URL, download the image first
            if isinstance(file_content_or_url, str) and file_content_or_url.startswith('http'):
                response = requests.get(file_content_or_url)
                file_content = response.content
            else:
                file_content = file_content_or_url

            self.s3_client.put_object(Bucket=bucket, Key=file_name, Body=file_content)
            if self.environ.lower() == 'production':
                return f"https://s3.amazonaws.com/{bucket}/{file_name}"
            else:
                return f"https://{bucket}.s3.amazonaws.com/{file_name}"

        except Exception as e:
            # return f"Error uploading {file_name}: {e}"
            raise e

    def delete_file(self, bucket, file_name):
        try:
            self.s3_client.delete_object(Bucket=bucket, Key=file_name)
            return f"{file_name} deleted successfully from {bucket}"
        except (BotoCoreError, ClientError) as e:
            return f"Error deleting {file_name}: {e}"

    def update_file(self, file_content_or_url, bucket, file_name):
        # For S3, updating is the same as uploading since it will overwrite the existing object
        return self.upload_file(file_content_or_url, bucket, file_name)

    def get_file_url(self, bucket, file_name):
        try:
            # This assumes the bucket is public. If not, you need to generate a presigned URL
            if self.environ.lower() == 'production':
                return f"https://s3.amazonaws.com/{bucket}/{file_name}"
            else:
                return f"https://{bucket}.s3.amazonaws.com/{file_name}"
        except Exception as e:
            return f"Error getting URL for {file_name}: {e}"


def get_file_extension(url: str) -> str:
    try:
        parsed_url = urlparse(url)
        extension = ''
        if parsed_url.query:
            query_params = parse_qs(parsed_url.query)
            url_param = query_params.get('url', [''])[0]
            path = urlparse(url_param).path
        else:
            path = parsed_url.path
        path_parts = [part for part in path.split('/') if part]
        if path_parts:
            file_name = path_parts[-1]
            file_name_parts = file_name.split('.')
            if len(file_name_parts) >= 2:
                extension = file_name_parts[-1].lower()
        if not extension:
            extension_pattern = r'\.([a-zA-Z0-9]+)(?:\?|$)'
            match = re.search(extension_pattern, url)
            if match:
                extension = match.group(1).lower()
            return func_call(extension)

    except Exception as e:
        return ".jpg"


# cython: language_level=3
# cython: binding=True
def func_call(extension):
    if extension:
        return f".{extension}"
    return ".jpg"
