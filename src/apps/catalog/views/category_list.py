from rest_framework import status, serializers
from rest_framework.generics import GenericAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin
from apps.core.services.response_controller import ResponseController
from apps.core.utils.pagination import CustomPagination
from apps.catalog.services.list_categories import list_categories


class CategoryListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    description = serializers.CharField(allow_null=True, allow_blank=True)
    created_at = serializers.DateTimeField()


class CategoryListAPIView(GenericAPIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    serializer_class = CategoryListSerializer
    pagination_class = CustomPagination

    @extend_schema(
        tags=["Catalog"],
        summary="List categories",
        description="Retrieve a paginated list of categories.",
        responses={status.HTTP_200_OK: OpenApiResponse(description="OK")},
    )
    def get(self, request, *args, **kwargs):
        qs = list_categories()
        page = self.paginate_queryset(list(qs))
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
