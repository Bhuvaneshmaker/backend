from rest_framework import serializers


class TelemetryPacketSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    device_id = serializers.IntegerField()
    frame_type = serializers.IntegerField()
    checksum_valid = serializers.BooleanField()
    source_ip = serializers.CharField()
    received_at = serializers.CharField(read_only=True)
    elevators = serializers.ListField()


class ElevatorStateSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    device_id = serializers.IntegerField()
    device_pk = serializers.CharField(required=False)
    slave_id = serializers.IntegerField()
    connection_status = serializers.CharField()
    overload = serializers.BooleanField(allow_null=True)
    mimo = serializers.BooleanField(allow_null=True)
    independent_mode = serializers.BooleanField(allow_null=True)
    run_stop = serializers.CharField()
    fireman_switch_status = serializers.BooleanField(allow_null=True)
    fire_emergency_status = serializers.BooleanField(allow_null=True)
    fire_emergency_return_status = serializers.BooleanField(allow_null=True)
    malfunction = serializers.BooleanField(allow_null=True)
    door_status = serializers.CharField()
    lift_direction_up = serializers.BooleanField(allow_null=True)
    lift_direction_down = serializers.BooleanField(allow_null=True)
    lift_position = serializers.IntegerField(allow_null=True)
    updated_at = serializers.CharField(read_only=True)
