from rest_framework import status, serializers
from rest_framework.generics import GenericAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated
from apps.core.services.docs import common_responses
from apps.bazars.services.get_place_by_qr import get_place_by_qr
from apps.core.services.response_controller import ResponseController


class GetPlaceByQRSerializer(serializers.Serializer):
    qr_text = serializers.CharField(max_length=255)


class GetPlaceByQRAPIView(GenericAPIView, ResponseController):
    serializer_class = GetPlaceByQRSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Places"],
        summary="Get Place by QR code",
        description="Return Place information using qr_text. QR must be valid.",
        request=GetPlaceByQRSerializer,
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                description="Place retrieved by QR code",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "Place retrieved successfully.",
                            "data": {
                                "id": 10,
                                "bazar_id": 3,
                                "number": 5,
                                "is_active": True,
                                "qr_code": {
                                    "qr_text": "QR-12345",
                                    "generate_at": "2025-12-12T10:00:00Z",
                                    "valid": True
                                },
                                "products": [
                                    {"id": 1, "name": "Apple", "price": "10000.00", "quantity": 10}
                                ]
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

        data = get_place_by_qr(
            **serializer.validated_data
        )

        return self.success_response(
            data=data,
            status=status.HTTP_200_OK
        )
