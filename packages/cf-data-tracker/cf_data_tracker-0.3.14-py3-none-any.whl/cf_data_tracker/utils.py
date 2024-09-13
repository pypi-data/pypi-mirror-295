import boto3
import os
from dotenv import load_dotenv
load_dotenv()

S3_CLIENT = boto3.client(
    "s3",
    region_name=os.environ.get('AWS_REGION_NAME','eu-west-2'),
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
)