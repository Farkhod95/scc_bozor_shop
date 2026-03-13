from rest_framework import status, serializers
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.core.auth.authentication import JWTAuthentication
from apps.core.services.docs import common_responses
from apps.core.services.response_controller import ResponseController
from apps.bazars.services.list_bazar_images import list_bazar_images
from apps.core.utils.pagination import CustomPagination


class BazarImageListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    image = serializers.CharField()
    is_main = serializers.BooleanField()


class ListBazarImageAPIView(ListAPIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = []
    serializer_class = BazarImageListSerializer
    pagination_class = CustomPagination

    @extend_schema(
        tags=["Bazar Images"],
        summary="List bazar images",
        description="Get all images of a bazar. Main image is returned first.",
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                response=BazarImageListSerializer(many=True),
                description="Bazar images retrieved successfully.",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "OK",
                            "links": {
                                "next": None,
                                "previous": None,
                            },
                            "pagination": {
                                "current_page": 1,
                                "total_pages": 1,
                                "page_size": 10,
                                "total_items": 1,
                            },
                            "data": [
                                {
                                    "id": 1,
                                    "image": "http://example.com/media/uploads/bazar1.jpg",
                                    "is_main": True
                                },
                                {
                                    "id": 2,
                                    "image": "http://example.com/media/uploads/bazar2.jpg",
                                    "is_main": False
                                }
                            ],
                        },
                    )
                ]
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        bazar_id = kwargs.get("pk")

        data = list_bazar_images(bazar_id=bazar_id)

        page = self.paginate_queryset(data)
        return self.get_paginated_response(page)
