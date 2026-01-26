from rest_framework import serializers, status
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.bazars.services.list_place_product import list_place_product
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin, IsAdmin
from apps.core.services.docs import common_responses
from apps.core.services.response_controller import ResponseController
from apps.core.utils.pagination import CustomPagination


class ListPlaceProductSerializer(serializers.Serializer):
    bazar_id = serializers.IntegerField(required=False)
    product_id = serializers.IntegerField(required=False)


class ListPlaceProductAPIView(ListAPIView, ResponseController):
    serializer_class = ListPlaceProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination


    @extend_schema(
        tags=["PlaceProduct"],
        summary="List PlaceProducts",
        description="List all PlaceProducts or filter by bazar_id.",
        parameters=[ListPlaceProductSerializer],
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                response=ListPlaceProductSerializer,
                description="PlaceProducts retrieved successfully",
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
                                    "place_id": 3,
                                    "place_number": 12,
                                    "product_id": 5,
                                    "product_name": "Apple",
                                    "product_photo": "file/mathematics.jpg",
                                    "price": "100.00",
                                    "quantity": 10
                                }
                            ],
                        }
                    )
                ]
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        bazar_id = request.query_params.get("bazar_id")
        product_id = request.query_params.get("product_id")
        bazar_id = int(bazar_id) if bazar_id is not None else None
        product_id = int(product_id) if product_id is not None else None

        data = list_place_product(request.user, request.lang,bazar_id=bazar_id, product_id=product_id)
        page = self.paginate_queryset(data)
        return self.get_paginated_response(page)

