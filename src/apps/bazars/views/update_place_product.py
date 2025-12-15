from rest_framework import serializers, status
from rest_framework.generics import UpdateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.bazars.services.update_place_product import update_place_product
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin, IsAdmin
from apps.core.services.docs import common_responses
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message


class UpdatePlaceProductSerializer(serializers.Serializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    quantity = serializers.IntegerField(required=False, min_value=1)


class UpdatePlaceProductAPIView(UpdateAPIView, ResponseController):
    http_method_names = ["patch"]
    serializer_class = UpdatePlaceProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, (IsSuperAdmin | IsAdmin)]

    @extend_schema(
        tags=["PlaceProduct"],
        summary="Update PlaceProduct",
        description="Update price or quantity of a PlaceProduct. Previous price is stored in PlacePriceHistory.",
        request=UpdatePlaceProductSerializer,
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                description="PlaceProduct updated successfully",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "PlaceProduct updated successfully",
                            "data": {
                                "id": 1,
                                "place": 3,
                                "product": 5,
                                "price": "150.00",
                                "quantity": 20
                            }
                        }
                    )
                ]
            ),
        },
    )
    def patch(self, request, *args, **kwargs):
        place_product_id = kwargs.get("pk")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = update_place_product(
            **serializer.validated_data,
            place_product_id=place_product_id,
            updated_by=request.user
        )

        return self.success_response(
            message=Message.CATEGORY_CREATED_SUCCESSFULLY,
            data=data,
            status=status.HTTP_200_OK
        )
