import httpx
import os
from config import WEATHER_API_KEY, BASE_URL


async def fetch_weather(city: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            BASE_URL,
            params={"q": city, "appid": WEATHER_API_KEY, "units": "metric"},
        )
        return response
