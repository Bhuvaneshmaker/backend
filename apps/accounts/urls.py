from django.urls import path

from .views import LoginView, MeView, PushTokenView, RefreshView, UserListView


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshView.as_view(), name="refresh"),
    path("me/", MeView.as_view(), name="me"),
    path("users/", UserListView.as_view(), name="users"),
    path("push-token/", PushTokenView.as_view(), name="push-token"),
]
