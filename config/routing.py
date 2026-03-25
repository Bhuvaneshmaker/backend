from django.urls import path

from apps.alerts.consumers import AlertsConsumer
from apps.telemetry.consumers import BlockConsumer, DeviceConsumer, ElevatorConsumer


websocket_urlpatterns = [
    path("ws/alerts/", AlertsConsumer.as_asgi()),
    path("ws/blocks/<str:block_id>/", BlockConsumer.as_asgi()),
    path("ws/devices/<str:device_id>/", DeviceConsumer.as_asgi()),
    path("ws/elevators/<str:elevator_id>/", ElevatorConsumer.as_asgi()),
]
