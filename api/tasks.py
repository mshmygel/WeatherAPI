from celery import shared_task
import os
import requests
from .models import WeatherData


@shared_task
def fetch_weather_data(city):
    """
    Celery task that fetches weather data from a public API and
    CREATES a new WeatherData row each time (for historical storage).
    """
    api_key = os.getenv("WEATHER_API_KEY")
    base_url = os.getenv("WEATHER_API_URL", "https://api.openweathermap.org/data/2.5/weather")

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "en",
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()

    data = response.json()

    # Always create a new historical row
    WeatherData.objects.create(
        city=data["name"],
        temperature=data["main"]["temp"],
        humidity=data["main"]["humidity"],
        wind_speed=data["wind"]["speed"],
        description=data["weather"][0]["description"]
    )
