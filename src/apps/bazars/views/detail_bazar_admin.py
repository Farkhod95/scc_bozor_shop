from rest_framework import status, serializers
from rest_framework.generics import RetrieveAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsSuperAdmin, IsAuthenticated, IsAdmin, IsManager
from apps.core.services.docs import common_responses
from apps.bazars.services.detail_bazar_admin import detail_bazar_admin
from apps.core.services.response_controller import ResponseController

class DetailBazarAdminSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    bazar_id = serializers.IntegerField()
    bazar_name_uz = serializers.CharField()
    bazar_name_ru = serializers.CharField()
    bazar_name_en = serializers.CharField()
    bazar_name_uz_cyrl = serializers.CharField()
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    assigned_at = serializers.DateTimeField()


class DetailBazarAdminAPIView(RetrieveAPIView, ResponseController):
    serializer_class = DetailBazarAdminSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, (IsSuperAdmin | IsManager)]
    lookup_url_kwarg = "bazar_admin_id"

    @extend_schema(
        tags=["Bazar Admins"],
        summary="Retrieve a Bazar Admin",
        description="Get detailed information of a specific Bazar Admin by ID.",
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                response=DetailBazarAdminSerializer,
                description="Bazar Admin details",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "Bazar admin retrieved successfully.",
                            "data": {
                                "id": 1,
                                "bazar_id": 1,
                                "bazar_name": "Central Bazar",
                                "user_id": 2,
                                "username": "admin_user",
                                "assigned_at": "2025-12-12T10:00:00Z"
                            }
                        }
                    )
                ]
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        bazar_admin_id = kwargs.get("pk")
        data = detail_bazar_admin(bazar_admin_id)
        return self.success_response(
            data=data,
            status=status.HTTP_200_OK
        )
