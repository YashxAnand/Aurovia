import os
import boto3
from botocore.exceptions import ClientError
import uuid

def get_s3_client():
    access_key = os.getenv("R2_ACCESS_KEY_ID")
    secret_key = os.getenv("R2_SECRET_ACCESS_KEY")
    endpoint = os.getenv("R2_ENDPOINT_URL")

    if not all([access_key, secret_key, endpoint]):
        return None

    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="auto",
        config=boto3.session.Config(signature_version='s3v4')
    )

def upload_file_to_r2(file_content, filename, content_type):
    s3_client = get_s3_client()
    bucket = os.getenv("R2_BUCKET_NAME")
    public_url_base = os.getenv("R2_PUBLIC_URL", "").rstrip("/")
    
    if not s3_client or not bucket:
        # Fallback for development if S3 not configured
        # Or return None/Error
        raise ValueError("R2 configuration is missing")

    # Generate unique key to prevent overwrites
    ext = filename.split(".")[-1]
    unique_key = f"{uuid.uuid4().hex}.{ext}"
    
    try:
        s3_client.put_object(
            Bucket=bucket,
            Key=unique_key,
            Body=file_content,
            ContentType=content_type
        )
        url = f"{public_url_base}/{unique_key}" if public_url_base else f"https://{bucket}.r2.cloudflarestorage.com/{unique_key}"
        return unique_key, url
    except ClientError as e:
        print(f"Failed to upload to R2: {e}")
        return None, None

def delete_file_from_r2(key):
    if not key:
        return
        
    s3_client = get_s3_client()
    bucket = os.getenv("R2_BUCKET_NAME")
    
    if not s3_client or not bucket:
        return
        
    try:
        s3_client.delete_object(Bucket=bucket, Key=key)
    except ClientError as e:
        print(f"Failed to delete from R2: {e}")
