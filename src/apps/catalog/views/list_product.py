from rest_framework import serializers, permissions, status
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.catalog.services.list_product import list_products
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin
from apps.core.services.response_controller import ResponseController
from apps.core.services.docs import common_responses
from apps.core.utils.pagination import CustomPagination


class ListBazarQuerySerializer(serializers.Serializer):
    search = serializers.CharField(required=False)
    unit = serializers.CharField(required=False)
    category_id = serializers.IntegerField(required=False)


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
        parameters=[ListBazarQuerySerializer],
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
        query_serializer = ListBazarQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        filters = {k: v for k, v in query_serializer.validated_data.items() if k != "search"}
        search = query_serializer.validated_data.get("search")

        products = list_products(user=request.user, lang=request.lang, filters=filters, search=search)

        page = self.paginate_queryset(products)
        return self.get_paginated_response(page)
