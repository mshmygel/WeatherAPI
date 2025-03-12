import requests
import os
from django.core.management.base import BaseCommand
from api.models import WeatherData

class Command(BaseCommand):
    help = "Fetch weather data from OpenWeatherMap API and store it in the database"

    def add_arguments(self, parser):
        parser.add_argument("city", type=str, help="City name to fetch weather data for")

    def handle(self, *args, **kwargs):
        city = kwargs["city"]
        api_key = os.getenv("WEATHER_API_KEY")
        base_url = os.getenv("WEATHER_API_URL")

        params = {
            "q": city,
            "appid": api_key,
            "units": "metric",
            "lang": "en",
        }

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            weather = WeatherData.objects.create(
                city=data["name"],
                temperature=data["main"]["temp"],
                humidity=data["main"]["humidity"],
                wind_speed=data["wind"]["speed"],
                description=data["weather"][0]["description"],
            )
            self.stdout.write(self.style.SUCCESS(f"Successfully saved weather data for {weather.city}"))
        else:
            self.stdout.write(self.style.ERROR(f"Failed to fetch weather data: {response.text}"))
