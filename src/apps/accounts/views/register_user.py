from rest_framework import status, serializers
from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.accounts.services.register_user import register_user
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message


class RegisterRequestSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(min_length=6, write_only=True)
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phone_number = serializers.CharField(required=False, allow_blank=True)
    profile_image = serializers.IntegerField(required=False, allow_null=True)


class RegisterResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = serializers.DictField()


class RegisterUserAPIView(CreateAPIView, ResponseController):
    authentication_classes = []
    permission_classes = []
    serializer_class = RegisterRequestSerializer

    @extend_schema(
        tags=["Authentication"],
        summary="Register user",
        description="Create a new user account and return JWT tokens.",
        responses={
            status.HTTP_201_CREATED: OpenApiResponse(
                response=RegisterResponseSerializer,
                description="User registered successfully.",
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Validation error",
            ),
        },
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
                    "profile_image": "1",
                },
            ),
            OpenApiExample(
                "User disabled",
                value={
                    "detail": "This username is already taken."
                },
            ),
        ],
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = register_user(**serializer.validated_data)

        return self.success_response(
            message=Message.USER_REGISTERED,
            data=data,
            status=status.HTTP_201_CREATED
        )