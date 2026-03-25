from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import acknowledge_alert, list_alerts


class AlertListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, _request):
        return Response(list_alerts())


class AlertAcknowledgeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, alert_id: str):
        alert = acknowledge_alert(alert_id, request.user.username)
        if not alert:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(alert)
