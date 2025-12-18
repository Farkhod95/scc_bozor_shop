from rest_framework import status, serializers
from rest_framework.generics import UpdateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin, IsBazarAdmin
from apps.core.services.docs import common_responses
from apps.bazars.services.update_qrcode import update_qrcode
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message


class UpdateQRCodeSerializer(serializers.Serializer):
    place_id = serializers.IntegerField(required=False)
    qr_text = serializers.CharField(max_length=255, required=False)
    valid = serializers.BooleanField(required=False)


class UpdateQRCodeAPIView(UpdateAPIView, ResponseController):
    http_method_names = ["patch"]
    serializer_class = UpdateQRCodeSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, (IsSuperAdmin | IsBazarAdmin)]

    @extend_schema(
        tags=["QR Codes"],
        summary="Update QR code of a Place",
        description="Update QR code fields such as qr_text and valid by place_id.",
        request=UpdateQRCodeSerializer,
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                description="QR Code updated successfully.",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "QR code updated successfully.",
                            "data": {
                                "id": 1,
                                "place_id": 3,
                                "qr_text": "NEW-QR-789",
                                "generate_at": "2025-12-12T10:00:00Z",
                                "valid": True
                            }
                        }
                    )
                ]
            )
        }
    )
    def patch(self, request, *args, **kwargs):
        qrcode_id = kwargs.get("pk")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = update_qrcode(
            **serializer.validated_data,
            user=request.user,
            updated_by=request.user,
            qrcode_id=qrcode_id
        )

        return self.success_response(
            message=Message.QR_CODE_UPDATED_SUCCESSFULLY,
            data=data,
            status=status.HTTP_200_OK
        )
