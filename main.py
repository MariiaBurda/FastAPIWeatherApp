from fastapi import FastAPI, Query, HTTPException
import httpx
from dotenv import load_dotenv
import os
import json
import aioboto3 # for async work with s3
from datetime import datetime

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY is not set in the environment variables")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

async def save_to_s3(city: str, data: dict):
    filename = f"{city}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
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
    return filename


@app.get("/weather")
async def get_weather(city: str = Query(..., min_length=1)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                BASE_URL,
                params={"q": city, "appid": API_KEY, "units": "metric"},
            )

        if response.status_code == 200:
            data = response.json()
            filename = await save_to_s3(city, data)

            return {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "s3_file": filename,
            }
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="City not found")
        else:
            raise HTTPException(status_code=500, detail="Error fetching weather data")

    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while requesting data: {exc}"
        )
