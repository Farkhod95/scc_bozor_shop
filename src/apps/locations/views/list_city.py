from rest_framework import serializers, status
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.locations.services.list_city import list_city
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated
from apps.core.services.response_controller import ResponseController
from apps.core.services.docs import common_responses
from apps.core.utils.pagination import CustomPagination


class ListCityQuerySerializer(serializers.Serializer):
    search = serializers.CharField(required=False)


class ListCitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    code = serializers.CharField()
    region_id = serializers.IntegerField()
    created_at = serializers.DateTimeField()


class ListCityAPIView(ListAPIView, ResponseController):
    serializer_class = ListCitySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    @extend_schema(
        tags=["Cities"],
        summary="List cities",
        description="Retrieve all cities ordered by newest first.",
        parameters=[ListCityQuerySerializer],
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                response=ListCitySerializer(many=True),
                description="Cities retrieved successfully.",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "success": True,
                            "message": "Cities retrieved successfully.",
                            "data": [
                                {
                                    "id": 5,
                                    "name": "Namangan",
                                    "code": "NM",
                                    "region_id": 1,
                                    "created_at": "2025-12-11T12:00:00Z"
                                }
                            ]
                        }
                    )
                ]
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        query_serializer = ListCityQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        filters = {k: v for k, v in query_serializer.validated_data.items() if k != "search"}
        search = query_serializer.validated_data.get("search")

        cities = list_city(user=request.user, lang=request.lang, filters=filters, search=search)

        page = self.paginate_queryset(cities)
        return self.get_paginated_response(page)
