from rest_framework import serializers
from .models import WeatherData

class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = "__all__"

class CitySerializer(serializers.Serializer):
    city = serializers.CharField(required=True, max_length=100)