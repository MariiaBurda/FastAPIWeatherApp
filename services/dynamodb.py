import aioboto3

from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, DYNAMODB_TABLE


async def log_weather_event(city: str, timestamp: str, s3_url: str):
    session = aioboto3.Session()
    async with session.client(
        "dynamodb",
        region_name=AWS_REGION,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    ) as dynamodb:
        await dynamodb.put_item(
            TableName=DYNAMODB_TABLE,
            Item={
                "City": {"S": city},
                "Timestamp": {"S": timestamp},
                "S3URL": {"S": s3_url},
            },
        )
