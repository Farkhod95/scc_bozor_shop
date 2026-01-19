from rest_framework.generics import UpdateAPIView
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from apps.bazars.services.update_bazar import update_bazar
from rest_framework import serializers

from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin, IsManager
from apps.core.services.docs import common_responses
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message


class UpdateBazarSerializer(serializers.Serializer):
    name_uz = serializers.CharField(required=False)
    name_ru = serializers.CharField(required=False)
    name_en = serializers.CharField(required=False)
    name_uz_cyrl = serializers.CharField(required=False)
    city_id = serializers.IntegerField(required=False)
    address = serializers.CharField(required=False)
    lat = serializers.FloatField(required=False)
    lng = serializers.FloatField(required=False)


class UpdateBazarView(UpdateAPIView, ResponseController):
    http_method_names = ["patch"]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, (IsSuperAdmin | IsManager)]
    serializer_class = UpdateBazarSerializer

    @extend_schema(
        tags=["Bazars"],
        summary="Update Bazar",
        description="Update Bazar details and adjust places",
        request=UpdateBazarSerializer,
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                description="Bazar updated successfully.",
                examples=[
                    OpenApiExample(
                        name="Success Example",
                        value={
                            "success": True,
                            "message": "Bazar updated successfully.",
                            "data": {
                                "id": 10,
                                "name": "Updated Bazar",
                                "city_id": 2,
                                "address": "123 New Address",
                                "total_places": 50,
                                "created_at": "2025-01-12T09:30:00Z",
                            },
                        },
                        status_codes=[200],
                    ),
                ],
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Bazar or City not found."
            ),
        },
    )
    def patch(self, request, *args, **kwargs):
        product_id = kwargs.get("pk")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        data = update_bazar(
            bazar_id=product_id,
            updated_by=request.user,
            **serializer.validated_data,
        )

        return self.success_response(
            message=Message.BAZAR_CREATED_SUCCESSFULLY,
            data=data,
            status=status.HTTP_200_OK,
        )