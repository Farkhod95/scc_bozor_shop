from rest_framework import status
from rest_framework.generics import DestroyAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.locations.services.delete_city import delete_city
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin
from apps.core.services.response_controller import ResponseController
from apps.core.services.docs import common_responses
from apps.core.services.responses import Message


class DeleteCityAPIView(DestroyAPIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    @extend_schema(
        tags=["Cities"],
        summary="Delete city",
        description="Delete city by ID. Only SuperAdmin or Admin can delete cities.",
        responses={
            **common_responses,
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description="City deleted successfully.",
                examples=[
                    OpenApiExample(
                        "Not Found Example",
                        value={"detail": "City not found"},
                        status_codes=[404],
                    )
                ]
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="City not found."
            ),
        }
    )
    def delete(self, request, *args, **kwargs):
        city_id = kwargs.get("pk")
        delete_city(city_id)
        return self.success_response(
            message=Message.CITY_DELETED_SUCCESSFULLY,
            status=status.HTTP_200_OK
        )
