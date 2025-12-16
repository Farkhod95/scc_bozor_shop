
from rest_framework import serializers, permissions, status
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.catalog.services.list_subcategory import list_subcategory
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated
from apps.core.services.response_controller import ResponseController
from apps.core.services.docs import common_responses
from apps.core.utils.pagination import CustomPagination


class ListSubcategoryQuerySerializer(serializers.Serializer):
    search = serializers.CharField(required=False)
    category_id = serializers.IntegerField(required=False)


class ListSubcategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField(allow_null=True)
    created_at = serializers.DateTimeField()


class ListSubcategoryAPIView(ListAPIView, ResponseController):
    serializer_class = ListSubcategorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


    @extend_schema(
        tags=["Subcategories"],
        summary="List subcategories",
        description="Retrieve all subcategories ordered by newest first.",
        parameters=[ListSubcategoryQuerySerializer],
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                response=ListSubcategorySerializer(many=True),
                description="Subcategories retrieved successfully.",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "success": True,
                            "message": "Subcategories retrieved successfully.",
                            "data": [
                                {
                                    "id": 1,
                                    "title": "Fruits",
                                    "description": "All fruits items",
                                    "photo": "file/mathematics.jpg",
                                    "category_id": 3,
                                    "category_name": "Fruits",
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
        query_serializer = ListSubcategoryQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        filters = {k: v for k, v in query_serializer.validated_data.items() if k != "search"}
        search = query_serializer.validated_data.get("search")

        subcategories = list_subcategory(user=request.user, lang=request.lang, filters=filters, search=search)
        page = self.paginate_queryset(subcategories)
        return self.get_paginated_response(page)
