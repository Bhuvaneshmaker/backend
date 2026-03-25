from django.urls import path

from .views import GetDeviceIdView, GetSlaveIdView, SetDeviceIdView, SetSlaveIdView


urlpatterns = [
    path("get-device-id/", GetDeviceIdView.as_view(), name="get-device-id"),
    path("set-device-id/", SetDeviceIdView.as_view(), name="set-device-id"),
    path("get-slave-id/", GetSlaveIdView.as_view(), name="get-slave-id"),
    path("set-slave-id/", SetSlaveIdView.as_view(), name="set-slave-id"),
]
