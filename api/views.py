from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from .models import WeatherData
from .serializers import WeatherDataSerializer

class WeatherDataViewSet(viewsets.ModelViewSet):
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["city", "temperature"]
    ordering_fields = ["temperature", "humidity"]
