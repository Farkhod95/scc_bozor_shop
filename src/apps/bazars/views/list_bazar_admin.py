from rest_framework import status, serializers
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsSuperAdmin, IsAuthenticated, IsAdmin
from apps.core.services.docs import common_responses
from apps.bazars.services.list_bazar_admin import list_bazar_admins
from apps.core.services.response_controller import ResponseController


class ListBazarAdminSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    bazar_id = serializers.IntegerField()
    bazar_name = serializers.CharField()
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    assigned_at = serializers.DateTimeField()



class ListBazarAdminAPIView(ListAPIView, ResponseController):
    serializer_class = ListBazarAdminSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, (IsSuperAdmin | IsAdmin)]

    @extend_schema(
        tags=["Bazar Admins"],
        summary="List all Bazar Admins",
        description="Retrieve a list of all Bazar Admins with bazar and user information.",
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                response=ListBazarAdminSerializer,
                description="List of Bazar Admins",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "Bazar admins retrieved successfully.",
                            "data": [
                                {
                                    "id": 1,
                                    "bazar_id": 1,
                                    "bazar_name": "Central Bazar",
                                    "user_id": 2,
                                    "username": "admin_user",
                                    "assigned_at": "2025-12-12T10:00:00Z"
                                }
                            ]
                        }
                    )
                ]
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        data = list_bazar_admins()
        return self.success_response(
            data=data,
            status=status.HTTP_200_OK
        )
