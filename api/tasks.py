from celery import shared_task
import requests
from api.models import WeatherData

@shared_task
def fetch_weather_data(city):
    import requests
    import os

    api_key = os.getenv("WEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    response.raise_for_status()

    weather = response.json()

    from api.models import WeatherData

    obj = WeatherData.objects.create(
        city=weather["name"],
        temperature=weather["main"]["temp"],
        humidity=weather["main"]["humidity"],
        wind_speed=weather["wind"]["speed"],
        description=weather["weather"][0]["description"]
    )

    return obj.id
