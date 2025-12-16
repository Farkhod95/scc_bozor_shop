from rest_framework import status, serializers
from rest_framework.generics import RetrieveAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin, IsAdmin
from apps.core.services.docs import common_responses
from apps.bazars.services.detail_place import detail_place
from apps.core.services.response_controller import ResponseController


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    quantity = serializers.IntegerField()


class QRCodeSerializer(serializers.Serializer):
    qr_text = serializers.CharField()
    generate_at = serializers.DateTimeField()
    valid = serializers.BooleanField()


class DetailPlaceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    bazar_id = serializers.IntegerField()
    number = serializers.IntegerField()
    is_active = serializers.BooleanField()
    qr_code = QRCodeSerializer(allow_null=True)
    products = ProductSerializer(many=True)


class DetailPlaceAPIView(RetrieveAPIView, ResponseController):
    serializer_class = DetailPlaceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = []
    lookup_url_kwarg = "place_id"

    @extend_schema(
        tags=["Places"],
        summary="Retrieve a Place detail",
        description="Get detailed information of a Place including QR code and products.",
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                response=DetailPlaceSerializer,
                description="Place detail",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "Place retrieved successfully",
                            "data": {
                                "id": 1,
                                "bazar_id": 1,
                                "number": 1,
                                "is_active": True,
                                "qr_code": {
                                    "qr_text": "QR123",
                                    "generate_at": "2025-12-12T10:00:00Z",
                                    "valid": True
                                },
                                "products": [
                                    {
                                        "id": 1,
                                        "name": "Product1",
                                        "price": "100.00", "quantity": 2,
                                        "photo": "file/mathematics.jpg",
                                    }
                                ]
                            }
                        }
                    )
                ]
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        place_id = kwargs.get("pk")
        data = detail_place(place_id=int(place_id), lang=request.lang)
        return self.success_response(
            data=data,
            status=status.HTTP_200_OK
        )
