from rest_framework import status
from rest_framework.generics import DestroyAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.locations.services.delete_region import delete_region
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin, IsAdmin
from apps.core.services.response_controller import ResponseController
from apps.core.services.docs import common_responses
from apps.core.services.responses import Message


class DeleteRegionAPIView(DestroyAPIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, (IsSuperAdmin | IsAdmin)]

    @extend_schema(
        tags=["Regions"],
        summary="Delete region",
        description="Delete a region by its ID. Only SuperAdmin or Admin can delete regions.",
        responses={
            **common_responses,
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description="Region deleted successfully.",
                examples=[
                    OpenApiExample(
                        "Not Found Example",
                        value={"detail": "Region not found"},
                        status_codes=[404],
                    )
                ]
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Region not found."
            ),
        },
    )
    def delete(self, request, *args, **kwargs):
        region_id = kwargs.get("pk")

        delete_region(region_id)

        return self.success_response(
            message=Message.REGION_DELETED_SUCCESSFULLY,
            data=None,
            status=status.HTTP_204_NO_CONTENT
        )
