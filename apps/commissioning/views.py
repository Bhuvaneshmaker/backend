from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import DeviceIdRequestSerializer, SlaveIdRequestSerializer
from .services import create_job


class CommissioningActionView(APIView):
    permission_classes = [IsAuthenticated]
    action_name = ""
    serializer_class = None

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated = serializer.validated_data
        target_device = validated.pop("target_device")
        job = create_job(self.action_name, target_device, validated, request.user.username)
        return Response(job, status=status.HTTP_202_ACCEPTED)


class GetDeviceIdView(CommissioningActionView):
    action_name = "get_device_id"
    serializer_class = DeviceIdRequestSerializer


class SetDeviceIdView(CommissioningActionView):
    action_name = "set_device_id"
    serializer_class = DeviceIdRequestSerializer


class GetSlaveIdView(CommissioningActionView):
    action_name = "get_slave_id"
    serializer_class = SlaveIdRequestSerializer


class SetSlaveIdView(CommissioningActionView):
    action_name = "set_slave_id"
    serializer_class = SlaveIdRequestSerializer
