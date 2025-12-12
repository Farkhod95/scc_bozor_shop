from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.accounts.views import *

app_name = "accounts"

router = DefaultRouter()


urlpatterns = [
    # Authentication
    path("auth/login/", LoginAPIView.as_view(), name="login"),
    path("auth/register/", RegisterUserAPIView.as_view(), name="register"),
    path("auth/refresh-token/", RefreshTokenAPIView.as_view(), name="refresh-token"),

    # Profile
    path("users/me/", UserProfileAPIView.as_view(), name="user-profile"),

    # Users
    path("users/create/", CreateUserAPIView.as_view(), name="create-user"),
    path("users/<int:pk>/update/", UpdateUserAPIView.as_view(), name="update-user"),
    path("users/list/", ListUserAPIView.as_view(), name="list-users"),
    path("users/<int:pk>/detail/", UserDetailAPIView.as_view(), name="user-detail"),
    path("users/<int:pk>/delete/", DeleteUserAPIView.as_view(), name="delete-user"),
]