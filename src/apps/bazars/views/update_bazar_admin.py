from rest_framework import status,serializers
from rest_framework.generics import UpdateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsSuperAdmin, IsAuthenticated
from apps.core.services.docs import common_responses
from apps.bazars.services.update_bazar_admin import update_bazar_admin
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message


class UpdateBazarAdminSerializer(serializers.Serializer):
    bazar_id = serializers.IntegerField(required=False)
    user_id = serializers.IntegerField(required=False)

class UpdateBazarAdminAPIView(UpdateAPIView, ResponseController):
    http_method_names = ["patch"]
    serializer_class = UpdateBazarAdminSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    lookup_url_kwarg = "bazar_admin_id"

    @extend_schema(
        tags=["Bazar Admins"],
        summary="Update a Bazar Admin",
        description="Update the bazar or user of a specific Bazar Admin by ID.",
        request=UpdateBazarAdminSerializer,
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                response=UpdateBazarAdminSerializer,
                description="Bazar admin updated successfully.",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "Bazar admin updated successfully.",
                            "data": {
                                "id": 1,
                                "bazar_id": 2,
                                "bazar_name": "New Bazar",
                                "user_id": 3,
                                "username": "new_admin_user",
                                "assigned_at": "2025-12-12T10:00:00Z"
                            }
                        }
                    )
                ]
            ),
        },
    )
    def patch(self, request, *args, **kwargs):
        bazar_admin_id = kwargs.get("pk")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = update_bazar_admin(
            bazar_admin_id=bazar_admin_id,
            **serializer.validated_data
        )

        return self.success_response(
            message=Message.BAZAR_ADMIN_UPDATED_SUCCESSFULLY,
            data=data,
            status=status.HTTP_200_OK
        )
