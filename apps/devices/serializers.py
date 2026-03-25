from rest_framework import serializers


class DeviceSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    block_id = serializers.CharField(max_length=64)
    device_id = serializers.IntegerField(min_value=1, max_value=255)
    name = serializers.CharField(max_length=120)
    ip_address = serializers.CharField(max_length=64, required=False, allow_blank=True)
    mac_address = serializers.CharField(max_length=64, required=False, allow_blank=True)
    firmware_version = serializers.CharField(max_length=64, required=False, allow_blank=True)
    is_active = serializers.BooleanField(default=True)
    last_seen = serializers.CharField(read_only=True)
    status = serializers.CharField(required=False, allow_blank=True)


class SlaveBoardSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    device_id = serializers.CharField(max_length=64)
    slave_id = serializers.IntegerField(min_value=1, max_value=255)
    elevator_name = serializers.CharField(max_length=120)
    floors = serializers.IntegerField(min_value=0, max_value=255, required=False)
    is_active = serializers.BooleanField(default=True)
