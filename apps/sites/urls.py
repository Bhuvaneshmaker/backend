from django.urls import path

from .views import BlockDetailView, BlockListCreateView, SiteListCreateView


urlpatterns = [
    path("", SiteListCreateView.as_view(), name="sites"),
    path("blocks/", BlockListCreateView.as_view(), name="blocks"),
    path("blocks/<str:block_id>/", BlockDetailView.as_view(), name="block-detail"),
]
