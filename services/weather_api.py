import httpx

from config import WEATHER_API_KEY, BASE_URL
from tenacity import retry, stop_after_attempt, wait_fixed


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
async def fetch_weather(city: str):
    """
    Fetches weather data for the specified city from the weather API,
    retrying up to 3 times with a 2-second delay between attempts.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            BASE_URL,
            params={"q": city, "appid": WEATHER_API_KEY, "units": "metric"},
        )
        return response
