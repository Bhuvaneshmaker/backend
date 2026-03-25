from django.urls import path

from .views import DeviceDetailView, DeviceLatestStateView, DeviceListCreateView, SlaveBoardListCreateView


urlpatterns = [
    path("", DeviceListCreateView.as_view(), name="devices"),
    path("slaves/", SlaveBoardListCreateView.as_view(), name="slave-boards"),
    path("<str:device_pk>/", DeviceDetailView.as_view(), name="device-detail"),
    path("<str:device_pk>/latest-state/", DeviceLatestStateView.as_view(), name="device-latest-state"),
]
