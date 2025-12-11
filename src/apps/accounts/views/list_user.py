from rest_framework import status, serializers
from rest_framework.generics import GenericAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.accounts.services.list_user import list_users
from apps.core.auth.permissions import IsSuperAdmin, IsAuthenticated
from apps.core.auth.authentication import JWTAuthentication
from apps.core.services.docs import common_responses
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message
from apps.core.utils.pagination import CustomPagination


class ListUserQuerySerializer(serializers.Serializer):
    search = serializers.CharField(required=False)


class ListUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    profile_image = serializers.CharField(allow_null=True)


class ListUserAPIView(GenericAPIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    serializer_class = ListUserSerializer
    pagination_class = CustomPagination

    @extend_schema(
        tags=["Users"],
        summary="List users",
        description="Retrieve a list of all users.",
        parameters=[ListUserQuerySerializer],
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                response=ListUserSerializer,
                description="List of users retrieved successfully.",
                examples=[
                    OpenApiExample(
                        name="Success",
                        value=[
                            {
                                "message": "OK",
                                "links": {
                                    "next": "http://example.com/?page=2",
                                    "previous": None,
                                },
                                "pagination": {
                                    "current_page": 1,
                                    "total_pages": 12,
                                    "page_size": 10,
                                    "total_items": 120,
                                },
                                "data": [
                                    {
                                        "id": 1,
                                        "username": "ali01",
                                        "first_name": "Ali",
                                        "last_name": "Valiyev",
                                        "email": "ali01@gmail.com",
                                        "phone_number": "+998901234567",
                                        "profile_image": "http://example.uz/media/profile_images/ali01.jpg"
                                    }
                                ]
                            },
                        ],
                    ),
                ],
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        query_serializer = ListUserQuerySerializer(data=request.GET)
        query_serializer.is_valid(raise_exception=True)

        filters = {k: v for k, v in query_serializer.validated_data.items() if k != "search"}
        search = query_serializer.validated_data.get("search")

        data = list_users(filters=filters, search=search)

        page = self.paginate_queryset(data)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
