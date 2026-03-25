from django.urls import path

from .views import AlertAcknowledgeView, AlertListView


urlpatterns = [
    path("", AlertListView.as_view(), name="alerts"),
    path("<str:alert_id>/acknowledge/", AlertAcknowledgeView.as_view(), name="alert-acknowledge"),
]
