from rest_framework import status
from rest_framework.generics import DestroyAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.catalog.services.delete_subcategory import delete_subcategory
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin, IsAdmin
from apps.core.services.response_controller import ResponseController
from apps.core.services.docs import common_responses
from apps.core.services.responses import Message


class DeleteSubcategoryAPIView(DestroyAPIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, (IsSuperAdmin | IsAdmin)]

    @extend_schema(
        tags=["Subcategories"],
        summary="Delete subcategory",
        description="Delete subcategory by ID. Only SuperAdmin can delete subcategories.",
        responses={
            **common_responses,
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description="Subcategory deleted successfully.",
                examples=[
                    OpenApiExample(
                        "Not Found Example",
                        value={"detail": "Subcategory not found"},
                        status_codes=[404],
                    )
                ]
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Subcategory not found."
            ),
        }
    )
    def delete(self, request, *args, **kwargs):
        subcategory_id = kwargs.get("pk")
        delete_subcategory(subcategory_id)
        return self.success_response(
            message=Message.SUBCATEGORY_DELETED_SUCCESSFULLY,
            status=status.HTTP_200_OK
        )
