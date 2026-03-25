from django.urls import path

from .views import ElevatorHistoryView, LatestTelemetryView, TelemetryPacketDetailView, TelemetryPacketListView


urlpatterns = [
    path("latest/", LatestTelemetryView.as_view(), name="telemetry-latest"),
    path("packets/", TelemetryPacketListView.as_view(), name="telemetry-packets"),
    path("packets/<str:packet_id>/", TelemetryPacketDetailView.as_view(), name="telemetry-packet-detail"),
    path("elevators/<str:elevator_id>/history/", ElevatorHistoryView.as_view(), name="elevator-history"),
]
