from datetime import datetime, timezone, timedelta
import json
import aioboto3
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, S3_BUCKET_NAME


async def check_cache(city: str):
    session = aioboto3.Session()
    async with session.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    ) as s3:
        try:
            # get a list of objects that match the city_* pattern
            response = await s3.list_objects_v2(Bucket=S3_BUCKET_NAME, Prefix=f"{city}_")
            if "Contents" not in response:
                return None

            # find the newest file
            files = response["Contents"]
            latest_file = max(files, key=lambda x: x["LastModified"])

            # get data if last modification time is less than 5 minutes
            last_modified = latest_file["LastModified"].replace(tzinfo=timezone.utc)
            if datetime.now(timezone.utc) - last_modified < timedelta(minutes=5):
                obj = await s3.get_object(Bucket=S3_BUCKET_NAME, Key=latest_file["Key"])
                data = await obj["Body"].read()
                return json.loads(data)
            return None
        except Exception as e:
            print(f"Error checking cache: {e}")
            return None


async def save_to_s3(filename: str, data: dict):
    async with aioboto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    ) as s3:
        await s3.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=filename,
            Body=json.dumps(data),
            ContentType="application/json",
        )
