from rest_framework import status, serializers
from rest_framework.generics import UpdateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.locations.services.update_city import update_city
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin
from apps.core.services.docs import common_responses
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message


class UpdateCitySerializer(serializers.Serializer):
    name_uz = serializers.CharField(required=False, allow_blank=True)
    name_ru = serializers.CharField(required=False, allow_blank=True)
    name_en = serializers.CharField(required=False, allow_blank=True)
    name_uz_cyrl = serializers.CharField(required=False, allow_blank=True)
    code = serializers.CharField(required=False, allow_blank=True)
    region_id = serializers.IntegerField(required=False)


class UpdateCityAPIView(UpdateAPIView, ResponseController):
    http_method_names = ["patch"]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    serializer_class = UpdateCitySerializer

    @extend_schema(
        tags=["Cities"],
        summary="Update city",
        description="Updates an existing city. Only provided fields will be updated.",
        request=UpdateCitySerializer,
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                description="City updated successfully.",
                examples=[
                    OpenApiExample(
                        name="Success Example",
                        value={
                            "success": True,
                            "message": "City updated successfully.",
                            "data": {
                                "id": 5,
                                "name": "Updated City",
                                "code": "UC",
                                "region_id": 2,
                                "created_at": "2025-12-11T12:00:00Z",
                                "updated_at": "2025-12-11T14:00:00Z",
                            },
                        },
                        status_codes=[200],
                    )
                ],
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="City not found."
            ),
        },
    )
    def patch(self, request, *args, **kwargs):
        city_id = kwargs.get("pk")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = update_city(
            city_id=city_id,
            **serializer.validated_data
        )

        return self.success_response(
            message=Message.CITY_UPDATED_SUCCESSFULLY,
            data=data,
            status=status.HTTP_200_OK,
        )
