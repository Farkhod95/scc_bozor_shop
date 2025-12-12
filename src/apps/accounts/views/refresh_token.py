from rest_framework import status, permissions, serializers
from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.accounts.services.refresh_token import refresh_access_token
from apps.core.services.docs import common_responses
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True, help_text="Refresh token")


class RefreshTokenAPIView(CreateAPIView, ResponseController):
    serializer_class = RefreshTokenSerializer
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        tags=["Authentication"],
        summary="Refresh Access Token",
        description="Get a new access token by providing a valid refresh token.",
        request=RefreshTokenSerializer,
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                response=RefreshTokenSerializer,
                description="New access token generated successfully",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "Access token refreshed successfully",
                            "data": {
                                "access": "new_access_token_here"
                            }
                        }
                    )
                ]
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = refresh_access_token(
            refresh_token=serializer.validated_data["refresh"]
        )
        return self.success_response(
            message=Message.ACCESS_TOKEN_REFRESHED,
            data=data,
            status=status.HTTP_200_OK
        )
