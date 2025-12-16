from rest_framework import serializers, permissions, status
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.catalog.services.list_category import list_category
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin
from apps.core.services.response_controller import ResponseController
from apps.core.services.docs import common_responses
from apps.core.utils.pagination import CustomPagination


class ListCategoryQuerySerializer(serializers.Serializer):
    search = serializers.CharField(required=False)


class ListCategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField(allow_null=True)
    photo = serializers.URLField()
    created_at = serializers.DateTimeField()


class ListCategoryAPIView(ListAPIView, ResponseController):
    serializer_class = ListCategorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


    @extend_schema(
        tags=["Categories"],
        summary="List categories",
        description="Retrieve all categories ordered by newest first.",
        parameters=[ListCategoryQuerySerializer],
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                response=ListCategorySerializer(many=True),
                description="Categories retrieved successfully.",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "success": True,
                            "message": "Categories retrieved successfully.",
                            "data": [
                                {
                                    "id": 1,
                                    "title": "Fruits",
                                    "description": "All fruits items",
                                    "photo": "file/mathematics.jpg",
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
        query_serializer = ListCategoryQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        filters = {k: v for k, v in query_serializer.validated_data.items() if k != "search"}
        search = query_serializer.validated_data.get("search")

        categories = list_category(user=request.user, lang=request.lang, filters=filters, search=search)
        page = self.paginate_queryset(categories)
        return self.get_paginated_response(page)
