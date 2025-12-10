from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.accounts.services.detail_user import detail_user
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin
from apps.core.auth.authentication import JWTAuthentication
from apps.core.services.response_controller import ResponseController
from apps.core.services.docs import common_responses
from apps.core.services.responses import Message


class UserDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    profile_image = serializers.CharField(allow_null=True)
    role = serializers.CharField()


class UserDetailAPIView(GenericAPIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    serializer_class = UserDetailSerializer

    @extend_schema(
        tags=["Users"],
        summary="Get user detail",
        description="Retrieve detailed user information by ID.",
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                description="User retrieved successfully.",
                response=UserDetailSerializer,
                examples=[
                    OpenApiExample(
                        name="Success",
                        value={
                            "id": 1,
                            "username": "ali01",
                            "first_name": "Ali",
                            "last_name": "Valiyev",
                            "email": "ali01@gmail.com",
                            "phone_number": "+998901234567",
                            "profile_image": "http://example.uz/media/profile_images/ali01.jpg",
                            "role": "admin",
                        },
                    ),
                ],
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        data = detail_user(user_id)

        return self.success_response(
            data=data,
            status=status.HTTP_200_OK,
        )
