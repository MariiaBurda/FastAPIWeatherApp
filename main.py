from datetime import datetime

import httpx
from fastapi import FastAPI, Query, HTTPException

from config import (
    S3_BUCKET_NAME,
)
from services.dynamodb import log_weather_event
from services.s3 import check_cache, save_to_s3
from services.weather_api import fetch_weather

app = FastAPI()


@app.get("/weather")
async def get_weather(city: str = Query(..., min_length=1)):
    try:
        cached_data = await check_cache(city)
        if cached_data:
            return {
                "source": "cache",
                "city": cached_data["name"],
                "temperature": cached_data["main"]["temp"],
                "description": cached_data["weather"][0]["description"],
            }

        response = await fetch_weather(city)

        if response.status_code == 200:
            data = response.json()
            timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
            filename = f"{city}_{timestamp}.json"
            s3_url = f"s3://{S3_BUCKET_NAME}/{filename}"

            await save_to_s3(filename, data)
            await log_weather_event(city, timestamp, s3_url)

            return {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "s3_file": filename,
                "s3_url": s3_url,
            }
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="City not found")
        else:
            raise HTTPException(status_code=500, detail="Error fetching weather data")

    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while requesting data: {exc}"
        )
