from rest_framework import status, serializers
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsSuperAdmin, IsAuthenticated
from apps.core.services.docs import common_responses
from apps.bazars.services.list_bazar_admin import list_bazar_admins
from apps.core.services.response_controller import ResponseController
from apps.core.utils.pagination import CustomPagination


class ListBazarAdminSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    bazar_id = serializers.IntegerField()
    bazar_name = serializers.CharField()
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    assigned_at = serializers.DateTimeField()


class ListBazarAdminQuerySerializer(serializers.Serializer):
    search = serializers.CharField(required=False)
    bazar_id = serializers.IntegerField(required=False)


class ListBazarAdminAPIView(ListAPIView, ResponseController):
    serializer_class = ListBazarAdminSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    pagination_class = CustomPagination

    @extend_schema(
        tags=["Bazar Admins"],
        summary="List all Bazar Admins",
        description="Retrieve a list of all Bazar Admins with bazar and user information.",
        parameters=[ListBazarAdminQuerySerializer],
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                response=ListBazarAdminSerializer,
                description="List of Bazar Admins",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "OK",
                            "links": {
                                "next": "http://example.com/?page=2",
                                "previous": None,
                            },
                            "pagination": {
                                "current_page": 1,
                                "total_pages": 5,
                                "page_size": 10,
                                "total_items": 50,
                            },
                            "data": [
                                {
                                    "id": 1,
                                    "bazar_id": 1,
                                    "bazar_name": "Central Bazar",
                                    "user_id": 2,
                                    "username": "admin_user",
                                    "assigned_at": "2025-12-12T10:00:00Z"
                                }
                            ],
                        }
                    )
                ]
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        query_serializer = ListBazarAdminQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        filters = {k: v for k, v in query_serializer.validated_data.items() if k != "search"}
        search = query_serializer.validated_data.get("search")

        data = list_bazar_admins(
            filters=filters,
            search=search,
        )
        page = self.paginate_queryset(data)
        return self.get_paginated_response(page)
