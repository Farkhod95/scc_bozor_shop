from rest_framework import serializers, permissions, status
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.catalog.services.list_product import list_products
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin
from apps.core.services.response_controller import ResponseController
from apps.core.services.docs import common_responses
from apps.core.services.responses import Message
from apps.core.utils.pagination import CustomPagination


class ListProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    unit = serializers.CharField()
    category_id = serializers.IntegerField()
    category_name = serializers.CharField()
    created_at = serializers.DateTimeField()


class ListProductAPIView(ListAPIView, ResponseController):
    serializer_class = ListProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    @extend_schema(
        tags=["Products"],
        summary="List products",
        description="Retrieve all products ordered by newest first, including their category.",
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                response=ListProductSerializer(many=True),
                description="Products retrieved successfully.",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "success": True,
                            "message": "Products retrieved successfully.",
                            "data": [
                                {
                                    "id": 1,
                                    "name": "Laptop",
                                    "unit": "pcs",
                                    "category_id": 2,
                                    "category_name": "Electronics",
                                    "created_at": "2025-12-05T10:00:00Z"
                                }
                            ]
                        }
                    )
                ]
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        products = list_products(user=request.user, lang=request.lang)
        serializer = self.get_serializer(products, many=True)

        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)
