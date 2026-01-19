from rest_framework import status, serializers
from rest_framework.generics import UpdateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.accounts.services.update_user import update_user
from apps.core.auth.permissions import IsSuperAdmin, IsAuthenticated, IsManager
from apps.core.auth.authentication import JWTAuthentication
from apps.core.services.docs import common_responses
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message


class UpdateUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=False)
    password = serializers.CharField(min_length=6, write_only=True, required=False)
    email = serializers.EmailField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    profile_image = serializers.IntegerField(required=False, allow_null=True)


class UpdateUserAPIView(UpdateAPIView, ResponseController):
    http_method_names = ["patch"]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, (IsSuperAdmin | IsManager)]
    serializer_class = UpdateUserSerializer

    @extend_schema(
        tags=["Users"],
        summary="Update user",
        description="Update an existing user account.",
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                description="User updated successfully.",
                response=UpdateUserSerializer,
                examples=[
                    OpenApiExample(
                        "Success",
                        value={
                            "id": 1,
                            "username": "ali01",
                            "first_name": "Ali",
                            "last_name": "Valiyev",
                            "email": "ali01@gmail.com",
                            "phone_number": "+998901234567",
                            "profile_image": "http://example.uz/media/profile_images/ali01.jpg",
                        },
                    ),
                ],
            ),
        },
    )
    def patch(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = update_user(user_id, **serializer.validated_data)

        return self.success_response(
            data=data,
            message=Message.USER_UPDATED_SUCCESSFULLY,
            status=status.HTTP_200_OK,
        )
