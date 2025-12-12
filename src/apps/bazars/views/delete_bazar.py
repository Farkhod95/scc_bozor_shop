from rest_framework import status
from rest_framework.generics import DestroyAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.bazars.services.delete_bazar import delete_bazar
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin, IsAdmin
from apps.core.services.response_controller import ResponseController
from apps.core.services.docs import common_responses
from apps.core.services.responses import Message


class DeleteBazarAPIView(DestroyAPIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    @extend_schema(
        tags=["Bazars"],
        summary="Delete bazar",
        description="Delete a bazar by its ID. Only SuperAdmin can delete bazars.",
        responses={
            **common_responses,
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description="Bazar deleted successfully.",
                examples=[
                    OpenApiExample(
                        "Not Found Example",
                        value={"detail": "Bazar does not exist."},
                        status_codes=[400],
                    )
                ]
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Bazar not found."
            ),
        },
    )
    def delete(self, request, *args, **kwargs):
        bazar_id = kwargs.get("pk")

        delete_bazar(bazar_id)

        return self.success_response(
            message=Message.BAZAR_DELETED_SUCCESSFULLY,
            status=status.HTTP_200_OK
        )
