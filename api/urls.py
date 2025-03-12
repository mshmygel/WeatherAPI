from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WeatherDataViewSet, FetchWeatherAPIView, TaskStatusView

router = DefaultRouter()
router.register(r'weather', WeatherDataViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "fetch-weather/",
        FetchWeatherAPIView.as_view(),
        name="fetch-weather"
    ),
    path(
        "task-status/<uuid:task_id>/",
        TaskStatusView.as_view(),
        name="task-status"
    ),
]
