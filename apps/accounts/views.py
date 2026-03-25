from datetime import datetime, timezone

from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.common.mongo import get_collection

from .serializers import PushTokenSerializer, UserSerializer


push_tokens_collection = get_collection("push_tokens")


class LoginView(TokenObtainPairView):
    permission_classes = []


class RefreshView(TokenRefreshView):
    permission_classes = []


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, _request):
        users = User.objects.order_by("username")
        return Response(UserSerializer(users, many=True).data)


class PushTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PushTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payload = {
            **serializer.validated_data,
            "user_id": request.user.id,
            "username": request.user.username,
            "updated_at": datetime.now(timezone.utc),
        }
        push_tokens_collection.update_one(
            {"token": payload["token"]},
            {"$set": payload},
            upsert=True,
        )
        return Response({"status": "registered"})
