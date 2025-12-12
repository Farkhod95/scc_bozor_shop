from rest_framework.generics import CreateAPIView
from rest_framework import status, serializers
from drf_spectacular.utils import (
    extend_schema, OpenApiExample, OpenApiResponse
)

from apps.accounts.services.login import login
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class LoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class LoginAPIView(CreateAPIView, ResponseController):
    serializer_class = LoginSerializer
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        tags=["Authentication"],
        summary="Login user",
        description="Authenticate a user and return tokens.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=LoginSerializer,
                description="User logged in successfully.",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "Login successful.",
                            "data": {
                                "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                                "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                                "user": {
                                    "id": 12,
                                    "username": "admin01",
                                    "first_name": "Ali",
                                    "last_name": "Karimov",
                                    "email": "admin01@gmail.com",
                                    "phone_number": "+998901234567",
                                    "role": "admin",
                                },
                            }
                        },
                    )
                ],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=LoginSerializer,
                description="Username or password is incorrect.",
                examples=[
                    OpenApiExample(
                        "Incorrect",
                        value={
                            "detail": "Username or password is incorrect."
                        },
                    ),
                    OpenApiExample(
                        "User disabled",
                        value={
                            "detail": "User account is disabled."
                        },
                    ),

                ]
            ),
        },
    )
    def post(self, request, *args, **kwargs):

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = login(**serializer.validated_data)
        return self.success_response(message=Message.LOGIN_SUCCESS ,data=data)
