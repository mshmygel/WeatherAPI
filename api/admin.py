from django.contrib import admin
from .models import WeatherData

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ("city", "temperature", "humidity", "wind_speed", "description", "timestamp")
    search_fields = ("city", "description")
    list_filter = ("city", "timestamp")

