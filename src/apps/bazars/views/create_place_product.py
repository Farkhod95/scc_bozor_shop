from rest_framework import serializers, status
from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from apps.bazars.services.create_place_product import create_place_product
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin, IsBazarAdmin, IsManager
from apps.core.services.docs import common_responses
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message


class CreatePlaceProductSerializer(serializers.Serializer):
    place_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField(min_value=1)


class CreatePlaceProductAPIView(CreateAPIView, ResponseController):
    serializer_class = CreatePlaceProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, (IsSuperAdmin | IsBazarAdmin | IsManager)]

    @extend_schema(
        tags=["PlaceProduct"],
        summary="Create a product for a Place",
        description="Create a product inside a specific place with price and quantity.",
        request=CreatePlaceProductSerializer,
        responses={
            **common_responses,
            status.HTTP_201_CREATED: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="PlaceProduct created successfully",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "Place product created successfully",
                            "data": {
                                "id": 1,
                                "place": 3,
                                "product": 5,
                                "price": "120.00",
                                "quantity": 10
                            }
                        }
                    )
                ]
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = create_place_product(
            user=request.user,
            created_by=request.user,
            **serializer.validated_data
        )

        return self.success_response(
            message=Message.PLACE_PRODUCT_CREATED_SUCCESSFULLY,
            data=data,
            status=status.HTTP_201_CREATED
        )
