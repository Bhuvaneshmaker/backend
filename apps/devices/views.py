from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import DeviceSerializer, SlaveBoardSerializer
from .services import create_device, create_slave_board, get_device, get_latest_state_for_device, list_devices, list_slave_boards


class DeviceListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, _request):
        return Response(list_devices())

    def post(self, request):
        serializer = DeviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(create_device(serializer.validated_data), status=status.HTTP_201_CREATED)


class DeviceDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, _request, device_pk: str):
        device = get_device(device_pk)
        if not device:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        device["slaves"] = list_slave_boards(device_pk)
        return Response(device)


class DeviceLatestStateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, _request, device_pk: str):
        return Response({"device_id": device_pk, "states": get_latest_state_for_device(device_pk)})


class SlaveBoardListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        device_pk = request.query_params.get("device_id")
        return Response(list_slave_boards(device_pk))

    def post(self, request):
        serializer = SlaveBoardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(create_slave_board(serializer.validated_data), status=status.HTTP_201_CREATED)
