from rest_framework import status
from rest_framework.generics import DestroyAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.catalog.services.delete_product import delete_product
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin, IsAdmin
from apps.core.services.response_controller import ResponseController
from apps.core.services.docs import common_responses
from apps.core.services.responses import Message


class DeleteProductAPIView(DestroyAPIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, (IsSuperAdmin | IsAdmin)]

    @extend_schema(
        tags=["Products"],
        summary="Delete product",
        description="Delete a product by its ID. Only SuperAdmin can delete products.",
        responses={
            **common_responses,
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description="Product deleted successfully.",
                examples=[
                    OpenApiExample(
                        "Not Found Example",
                        value={"detail": "Product not found"},
                        status_codes=[404],
                    )
                ]
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Product not found."
            ),
        },
    )
    def delete(self, request, *args, **kwargs):
        product_id = kwargs.get("pk")

        delete_product(product_id)

        return self.success_response(
            message=Message.PRODUCT_DELETED_SUCCESSFULLY,
            status=status.HTTP_204_NO_CONTENT
        )
