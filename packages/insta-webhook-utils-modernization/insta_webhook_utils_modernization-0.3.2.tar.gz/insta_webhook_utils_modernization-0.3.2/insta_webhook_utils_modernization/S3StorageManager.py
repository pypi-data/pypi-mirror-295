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
