from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from celery.result import AsyncResult
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from django.utils import timezone
from datetime import timedelta

from .models import WeatherData
from .serializers import WeatherDataSerializer, CitySerializer
from .tasks import fetch_weather_data

class WeatherDataViewSet(viewsets.ModelViewSet):
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["city", "temperature"]
    ordering_fields = ["temperature", "humidity"]

    def get_queryset(self):
        """
        Return the newest record per city. We do .order_by('city','-timestamp')
        plus a .distinct('city') (Postgres only).
        """
        qs = WeatherData.objects.order_by("city", "-timestamp").distinct("city")
        return qs


class FetchWeatherAPIView(APIView):
    """
    POST /api/fetch-weather/
    Приймає { "city": "London" } і створює Celery-таску fetch_weather_data.
    """

    @swagger_auto_schema(
        request_body=CitySerializer,
        responses={
            202: openapi.Response("Accepted", CitySerializer),
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = CitySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        city = serializer.validated_data["city"]
        # Celery Task
        task = fetch_weather_data.delay(city)
        return Response({"task_id": task.id}, status=202)


class TaskStatusView(APIView):
    """
    GET /api/task-status/<task_id>/
    Перевірити статус Celery-завдання.
    """

    def get(self, request, task_id):
        result = AsyncResult(task_id)
        response_data = {
            "task_id": task_id,
            "status": result.status,
            "result": result.result if result.status == "SUCCESS" else None
        }
        return Response(response_data)


class WeatherHistoryAPIView(APIView):
    """
    GET /api/weather/history/?city=Kyiv&days=7

    Повертає всі записи (історію) з таблиці WeatherData
    для вказаного міста, за останні N днів (days=7 за замовчуванням).
    """

    def get(self, request):
        city = request.GET.get("city")
        if not city:
            return Response(
                {"error": "Parameter 'city' is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # default 7 days
        days_param = request.GET.get("days", 7)
        try:
            days = int(days_param)
        except ValueError:
            days = 7

        # timestamp > now - days
        since = timezone.now() - timedelta(days=days)

        queryset = WeatherData.objects.filter(
            city__iexact=city,
            timestamp__gte=since
        ).order_by("-timestamp")  # newest first

        serializer = WeatherDataSerializer(queryset, many=True)
        return Response(serializer.data)
