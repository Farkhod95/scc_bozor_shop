from rest_framework import status, serializers
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated
from apps.core.utils.pagination import CustomPagination
from apps.core.services.response_controller import ResponseController
from apps.core.services.docs import common_responses
from apps.locations.services.list_region import list_region


class ListRegionQuerySerializer(serializers.Serializer):
    search = serializers.CharField(required=False)


class ListRegionAPIView(ListAPIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    @extend_schema(
        tags=["Regions"],
        summary="List regions",
        description="Retrieve list of regions ordered by newest first.",
        parameters=[ListRegionQuerySerializer],
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                description="Regions retrieved successfully.",
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        query_serializer = ListRegionQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        search = query_serializer.validated_data.get("search")

        regions = list_region(
            user=request.user,
            lang=request.lang,
            filters=None,
            search=search
        )

        page = self.paginate_queryset(regions)
        return self.get_paginated_response(page)
