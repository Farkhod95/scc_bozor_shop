from rest_framework import status, serializers
from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin, IsAdmin
from apps.core.services.docs import common_responses
from apps.bazars.services.create_qrcode import create_qrcode
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message


class CreateQRCodeSerializer(serializers.Serializer):
    place_id = serializers.IntegerField()
    qr_text = serializers.CharField(max_length=255)


class CreateQRCodeAPIView(CreateAPIView, ResponseController):
    serializer_class = CreateQRCodeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, (IsSuperAdmin | IsAdmin)]

    @extend_schema(
        tags=["QR Codes"],
        summary="Create QR code for a Place",
        description="Generate a QR code for a specific Place by providing place_id and qr_text. "
                    "If the place already has a QR code, an error is returned.",
        request=CreateQRCodeSerializer,
        responses={
            **common_responses,
            status.HTTP_201_CREATED: OpenApiResponse(
                description="QR Code created successfully.",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "QR code created successfully.",
                            "data": {
                                "id": 1,
                                "place_id": 3,
                                "qr_text": "QR-123456",
                                "generate_at": "2025-12-12T10:00:00Z",
                                "valid": True
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

        data = create_qrcode(
            **serializer.validated_data,
            created_by=request.user,
        )

        return self.success_response(
            message=Message.QR_CODE_CREATED_SUCCESSFULLY,
            data=data,
            status=status.HTTP_201_CREATED
        )
