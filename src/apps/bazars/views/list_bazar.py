from rest_framework import status, serializers
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.bazars.services.list_bazar import list_bazar
from apps.core.services.response_controller import ResponseController
from apps.core.auth.authentication import JWTAuthentication
from apps.core.services.docs import common_responses
from apps.core.utils.pagination import CustomPagination


class ListBazarQuerySerializer(serializers.Serializer):
    search = serializers.CharField(required=False)
    city_id = serializers.IntegerField(required=False)


class ListBazarItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    city = serializers.CharField()
    region = serializers.CharField()
    address = serializers.CharField()
    total_places = serializers.IntegerField()


class ListBazarAPIView(ListAPIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = []
    pagination_class = CustomPagination

    @extend_schema(
        tags=["Bazars"],
        summary="List bazars",
        description="Return a list of bazars with optional city filter.",
        parameters=[ListBazarQuerySerializer],
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                response=ListBazarItemSerializer(many=True),
                description="Successful response with bazar list.",
                examples=[
                    OpenApiExample(
                        name="Success",
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
                                    "name": "Central Bazar",
                                    "city": "Tehran",
                                    "region": "Region 1",
                                    "address": "123 Main St",
                                    "total_places": 150,
                                    "lat": 35.6892,
                                    "lng": 51.3890,
                                    "distance": 2.5,
                                    "main_image": "http://example.com/media/main_image.jpg",
                                    "images": [
                                        {"id": 1, "url": "http://example.com/media/image1.jpg", "is_main": True},
                                        {"id": 2, "url": "http://example.com/media/image2.jpg", "is_main": False},
                                    ],
                                },
                                {
                                    "id": 2,
                                    "name": "Westside Bazar",
                                    "city": "Tehran",
                                    "region": "Region 2",
                                    "address": "456 Side St",
                                    "total_places": 100,
                                    "lat": 35.6892,
                                    "lng": 51.3890,
                                    "distance": 5.0,
                                    "main_image": "http://example.com/media/main_image2.jpg",
                                    "images": [
                                        {"id": 3, "url": "http://example.com/media/image3.jpg", "is_main": True},
                                    ],
                                },
                            ],
                        },
                    )
                ]
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        query_serializer = ListBazarQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        lat = query_serializer.validated_data.get("lat")
        lng = query_serializer.validated_data.get("lng")

        filters = {k: v for k, v in query_serializer.validated_data.items()
                   if k not in ["search", "lat", "lng"]}
        search = query_serializer.validated_data.get("search")

        data = list_bazar(
            user=request.user,
            lang=request.lang,
            filters=filters,
            search=search,
            user_coords={'lat': lat, 'lng': lng} if lat and lng else None
        )

        page = self.paginate_queryset(data)
        return self.get_paginated_response(page)