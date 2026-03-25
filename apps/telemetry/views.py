from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import get_elevator_history, get_latest_states, get_packet, list_packets


class LatestTelemetryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, _request):
        return Response(get_latest_states())


class TelemetryPacketListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        limit = int(request.query_params.get("limit", 50))
        return Response(list_packets(limit=limit))


class TelemetryPacketDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, _request, packet_id: str):
        packet = get_packet(packet_id)
        if not packet:
            return Response({"detail": "Not found."}, status=404)
        return Response(packet)


class ElevatorHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, elevator_id: str):
        limit = int(request.query_params.get("limit", 100))
        return Response(get_elevator_history(elevator_id, limit=limit))
