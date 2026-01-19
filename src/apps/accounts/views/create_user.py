from rest_framework import status, serializers, permissions
from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.accounts.services.create_user import create_user
from apps.core.auth.permissions import IsSuperAdmin, IsAuthenticated, IsManager
from apps.core.auth.authentication import JWTAuthentication
from apps.core.services.docs import common_responses
from apps.core.services.model_status import UserType
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(min_length=6, write_only=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    profile_image = serializers.IntegerField(required=False, allow_null=True)
    role = serializers.ChoiceField(required=False, choices=UserType.choices, default=UserType.ADMIN)


class CreateUserAPIView(CreateAPIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, (IsSuperAdmin | IsManager)]
    serializer_class = CreateUserSerializer

    @extend_schema(
        tags=["Users"],
        summary="Create user",
        description="Create a new user account.",
        responses={
            **common_responses,
            status.HTTP_201_CREATED: OpenApiResponse(
                response=CreateUserSerializer,
                description="User created successfully.",
                examples=[
                    OpenApiExample(
                        name="Success",
                        value={
                            "id": 1,
                            "username": "ali01",
                            "password": "strongpassword",
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
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = create_user(user=request.user, **serializer.validated_data)

        return self.success_response(
            data=data,
            message=Message.USER_CREATED_SUCCESSFULLY,
            status=status.HTTP_201_CREATED,
        )