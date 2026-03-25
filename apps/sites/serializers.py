from rest_framework import serializers


class SiteSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=120)
    customer_name = serializers.CharField(max_length=120, required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    created_at = serializers.CharField(read_only=True)
    updated_at = serializers.CharField(read_only=True)


class BlockSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    site_id = serializers.CharField(max_length=64)
    name = serializers.CharField(max_length=120)
    block_code = serializers.CharField(max_length=50)
    description = serializers.CharField(required=False, allow_blank=True)
    created_at = serializers.CharField(read_only=True)
    updated_at = serializers.CharField(read_only=True)
