import os
import boto3
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

def test_r2():
    access_key = os.getenv("R2_ACCESS_KEY_ID")
    secret_key = os.getenv("R2_SECRET_ACCESS_KEY")
    endpoint = os.getenv("R2_ENDPOINT_URL")

    client = boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="auto", # sometimes needed
        config=boto3.session.Config(signature_version='s3v4')
    )

    print("Listing buckets...")
    try:
        response = client.list_buckets()
        print("Buckets:")
        for bucket in response['Buckets']:
            print(f"  {bucket['Name']}")
    except Exception as e:
        print(f"Error listing buckets: {e}")

if __name__ == "__main__":
    test_r2()
