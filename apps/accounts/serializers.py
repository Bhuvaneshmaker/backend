from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")


class PushTokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=512)
    platform = serializers.ChoiceField(choices=["android", "ios"])
    provider = serializers.ChoiceField(choices=["expo", "fcm"], default="fcm")
    device_name = serializers.CharField(max_length=120, required=False, allow_blank=True)
