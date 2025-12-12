from rest_framework import serializers, status
from rest_framework.generics import DestroyAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.bazars.services.delete_place_product import delete_place_product
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin, IsAdmin
from apps.core.services.docs import common_responses
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message


class DeletePlaceProductAPIView(DestroyAPIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, (IsSuperAdmin | IsAdmin)]

    @extend_schema(
        tags=["PlaceProduct"],
        summary="Delete PlaceProduct",
        description="Delete a specific PlaceProduct by its ID.",
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                description="PlaceProduct deleted successfully",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "PlaceProduct deleted successfully",
                            "data": None
                        }
                    )
                ]
            ),
        },
    )
    def delete(self, request, *args, **kwargs):
        place_product_id = kwargs.get("pk")

        delete_place_product(
            place_product_id=place_product_id
        )

        return self.success_response(
            message=Message.PLACE_PRODUCT_DELETED_SUCCESSFULLY,
            status=status.HTTP_200_OK
        )
