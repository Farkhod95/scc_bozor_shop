from rest_framework.views import APIView
from rest_framework import serializers, permissions
from drf_spectacular.utils import OpenApiResponse, extend_schema

from apps.core.services.response_controller import ResponseController
from apps.core.services.docs import common_responses
from apps.core.auth.authentication import JWTAuthentication
from apps.accounts.services.user_profile import get_profile_data
from apps.core.services.responses import Message

class UserProfileSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    phone = serializers.CharField(max_length=50)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    role = serializers.IntegerField()
    language = serializers.CharField(required=False)
    profile_image = serializers.URLField()


class UserProfileAPIView(APIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializers_class = UserProfileSerializer

    @extend_schema(
        tags=["Users"],
        summary="Get User Profile",
        description="Retrieve the profile information of the authenticated user.",
        responses={
            **common_responses,
            200: OpenApiResponse(
                response=UserProfileSerializer,
                description="User profile retrieved successfully.",
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        profile_data = get_profile_data(user)
        return self.success_response(
            message=Message.USER_PROFILE_RETRIEVED,
            data=profile_data
        )