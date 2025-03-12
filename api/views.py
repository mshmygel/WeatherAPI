from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from celery.result import AsyncResult
from rest_framework.decorators import api_view

from .models import WeatherData
from .serializers import WeatherDataSerializer
from .tasks import fetch_weather_data


class WeatherDataViewSet(viewsets.ModelViewSet):
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["city", "temperature"]
    ordering_fields = ["temperature", "humidity"]


class FetchWeatherAPIView(APIView):
    def post(self, request):
        city = request.data.get("city")
        if not city:
            return Response({"error": "City is required."}, status=400)

        task = fetch_weather_data.delay(city)
        return Response({"task_id": task.id}, status=202)


class TaskStatusView(APIView):
    def get(self, request, task_id):
        result = AsyncResult(task_id)
        response_data = {
            "task_id": task_id,
            "status": result.status,
            "result": result.result if result.status == "SUCCESS" else None
        }
        return Response(response_data)
