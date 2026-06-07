import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Load env variables
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

def get_s3_client():
    access_key = os.getenv("R2_ACCESS_KEY_ID")
    secret_key = os.getenv("R2_SECRET_ACCESS_KEY")
    endpoint = os.getenv("R2_ENDPOINT_URL")

    if not all([access_key, secret_key, endpoint]):
        print("Missing R2 credentials in .env")
        return None

    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="auto",
        config=boto3.session.Config(signature_version='s3v4')
    )

def upload_all_assets():
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
    s3_client = get_s3_client()
    bucket = os.getenv("R2_BUCKET_NAME")
    
    if not s3_client or not bucket:
        print("Cannot proceed without S3 client or Bucket name")
        return

    supported_exts = {".jpg", ".jpeg", ".png"}
    count = 0
    
    for root, dirs, files in os.walk(assets_dir):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in supported_exts:
                filepath = os.path.join(root, file)
                
                # We upload with the exact filename as the Key
                key = file
                
                content_type = "image/jpeg"
                if ext == ".png":
                    content_type = "image/png"
                    
                print(f"Uploading {filepath} to {key}...")
                with open(filepath, "rb") as f:
                    file_content = f.read()
                    
                try:
                    s3_client.put_object(
                        Bucket=bucket,
                        Key=key,
                        Body=file_content,
                        ContentType=content_type
                    )
                    count += 1
                except ClientError as e:
                    print(f"Failed to upload {file}: {e}")
                    
    print(f"Successfully uploaded {count} assets to R2!")

if __name__ == "__main__":
    upload_all_assets()
