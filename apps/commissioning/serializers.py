from rest_framework import serializers


class CommissioningJobSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    action = serializers.ChoiceField(
        choices=["set_device_id", "get_device_id", "set_slave_id", "get_slave_id"]
    )
    target_device = serializers.CharField(max_length=64)
    payload = serializers.DictField(required=False)
    status = serializers.CharField(read_only=True)
    requested_by = serializers.CharField(read_only=True)
    created_at = serializers.CharField(read_only=True)


class DeviceIdRequestSerializer(serializers.Serializer):
    target_device = serializers.CharField(max_length=64)
    device_id = serializers.IntegerField(min_value=1, max_value=255, required=False)


class SlaveIdRequestSerializer(serializers.Serializer):
    target_device = serializers.CharField(max_length=64)
    slave_id = serializers.IntegerField(min_value=1, max_value=255, required=False)
    new_slave_id = serializers.IntegerField(min_value=1, max_value=255, required=False)
