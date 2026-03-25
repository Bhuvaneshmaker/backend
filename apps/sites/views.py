from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import BlockSerializer, SiteSerializer
from .services import create_block, create_site, get_block, list_blocks, list_sites, update_block


class SiteListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, _request):
        return Response(list_sites())

    def post(self, request):
        serializer = SiteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(create_site(serializer.validated_data), status=status.HTTP_201_CREATED)


class BlockListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, _request):
        return Response(list_blocks())

    def post(self, request):
        serializer = BlockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(create_block(serializer.validated_data), status=status.HTTP_201_CREATED)


class BlockDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, _request, block_id: str):
        block = get_block(block_id)
        if not block:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(block)

    def patch(self, request, block_id: str):
        serializer = BlockSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated = update_block(block_id, serializer.validated_data)
        if not updated:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(updated)
