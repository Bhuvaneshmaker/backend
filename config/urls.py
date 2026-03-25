from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from django.utils import timezone


def health_check(_request):
    return JsonResponse(
        {
            "status": "ok",
            "service": "elevator-ems-backend",
            "timestamp": timezone.now().isoformat(),
        }
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health_check, name="health"),
    path("api/health/", health_check, name="api-health"),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/sites/", include("apps.sites.urls")),
    path("api/devices/", include("apps.devices.urls")),
    path("api/telemetry/", include("apps.telemetry.urls")),
    path("api/alerts/", include("apps.alerts.urls")),
    path("api/commissioning/", include("apps.commissioning.urls")),
]
