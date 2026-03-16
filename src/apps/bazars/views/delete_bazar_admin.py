from rest_framework import status
from rest_framework.generics import DestroyAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsSuperAdmin, IsAuthenticated, IsAdmin, IsManager
from apps.core.services.docs import common_responses
from apps.bazars.services.delete_bazar_admin import delete_bazar_admin
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message


class DeleteBazarAdminAPIView(DestroyAPIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, (IsSuperAdmin | IsManager)]
    lookup_url_kwarg = "bazar_admin_id"

    @extend_schema(
        tags=["Bazar Admins"],
        summary="Delete a Bazar Admin",
        description="Delete a specific Bazar Admin by ID.",
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Bazar admin deleted successfully.",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "Bazar admin deleted successfully.",
                            "data": None
                        }
                    )
                ]
            ),
        },
    )
    def delete(self, request, *args, **kwargs):
        bazar_admin_id = kwargs.get("pk")
        delete_bazar_admin(bazar_admin_id)
        return self.success_response(
            message=Message.BAZAR_ADMIN_DELETED_SUCCESSFULLY,
            status=status.HTTP_200_OK
        )
