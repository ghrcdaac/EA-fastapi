from dotenv import load_dotenv
import os

load_dotenv()

s3Url = os.environ.get('EA_FASTAPI_S3_URL')
s3BucketName = os.environ.get('EA_FASTAPI_S3_BUCKET')
s3ObjectUrl = os.environ.get('EA_FASTAPI_S3_OBJECT_URL')
fileDownloadPath = os.environ.get('EA_FASTAPI_FILE_DOWNLOAD_PATH')
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')