from rest_framework import serializers


class AlertSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    device_id = serializers.IntegerField()
    slave_id = serializers.IntegerField(required=False, allow_null=True)
    severity = serializers.CharField(max_length=20)
    code = serializers.CharField(max_length=50)
    title = serializers.CharField(max_length=120)
    message = serializers.CharField()
    acknowledged = serializers.BooleanField(default=False)
    acknowledged_by = serializers.CharField(required=False, allow_blank=True)
    resolved_at = serializers.CharField(required=False, allow_blank=True)
    created_at = serializers.CharField(read_only=True)
