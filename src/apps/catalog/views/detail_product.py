from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.exceptions import NotFound
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.catalog.services.detail_product import get_product_detail
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin
from apps.core.services.response_controller import ResponseController
from apps.core.services.docs import common_responses


class DetailProductAPIView(RetrieveAPIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Products"],
        summary="Get product detail",
        description="Returns detailed information about a product by its ID.",
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                description="Product detail returned successfully.",
                examples=[
                    OpenApiExample(
                        name="Success",
                        value={
                            "success": True,
                            "data": {
                                "id": 1,
                                "category": 3,
                                "name": "Apple",
                                "unit": "kg",
                                "created_at": "2025-01-15T12:00:30Z"
                            }
                        },
                        status_codes=[200],
                    )
                ],
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Product not found."
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        product_id = kwargs.get("pk")

        data = get_product_detail(product_id=product_id)

        return self.success_response(
            data=data,
            status=status.HTTP_200_OK
        )
