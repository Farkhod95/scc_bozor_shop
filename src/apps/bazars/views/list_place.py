from rest_framework import status, serializers
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin, IsAdmin
from apps.core.services.docs import common_responses
from apps.bazars.services.list_place import list_places
from apps.core.services.response_controller import ResponseController
from apps.core.utils.pagination import CustomPagination


class ListPlaceRequestSerializer(serializers.Serializer):
    bazar_id = serializers.IntegerField(required=True)


class QRCodeSerializer(serializers.Serializer):
    qr_text = serializers.CharField()
    generate_at = serializers.DateTimeField()
    valid = serializers.BooleanField()


class ListPlaceSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    number = serializers.IntegerField()
    is_active = serializers.BooleanField()
    qr_code = QRCodeSerializer(allow_null=True)


class ListPlaceAPIView(ListAPIView, ResponseController):
    serializer_class = ListPlaceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = []
    pagination_class = CustomPagination

    @extend_schema(
        tags=["Places"],
        summary="List all Places for a Bazar",
        description="Retrieve all places for a specific bazar including QR codes and products.",
        parameters=[ListPlaceRequestSerializer],
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                response=ListPlaceSerializer,
                description="List of places with QR code and products",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "Places retrieved successfully",
                            "data": [
                                {
                                    "id": 1,
                                    "number": 1,
                                    "is_active": True,
                                    "qr_code": {
                                        "qr_text": "QR123",
                                        "generate_at": "2025-12-12T10:00:00Z",
                                        "valid": True
                                    },
                                }
                            ]
                        }
                    )
                ]
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        bazar_id = request.query_params.get("bazar_id")

        data = list_places(bazar_id=int(bazar_id))

        page = self.paginate_queryset(data)
        return self.get_paginated_response(page)

