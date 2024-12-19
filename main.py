from fastapi import FastAPI, Query, HTTPException
import httpx
from dotenv import load_dotenv
import os


load_dotenv()

app = FastAPI()

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("API_KEY is not set in the environment variables")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

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
            return {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
            }
        elif response.status_code == 404:
            raise HTTPException(status_code=404, detail="City not found")
        else:
            raise HTTPException(status_code=500, detail="Error fetching weather data")

    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=500, detail=f"An error occurred while requesting data: {exc}"
        )
