from rest_framework import status, serializers
from rest_framework.generics import UpdateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.locations.services.update_region import update_region
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin, IsAdmin
from apps.core.services.docs import common_responses
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message


class UpdateRegionSerializer(serializers.Serializer):
    name_uz = serializers.CharField(required=False, allow_blank=True)
    name_ru = serializers.CharField(required=False, allow_blank=True)
    name_en = serializers.CharField(required=False, allow_blank=True)
    name_uz_cyrl = serializers.CharField(required=False, allow_blank=True)
    code = serializers.CharField(required=False, allow_blank=True)


class UpdateRegionAPIView(UpdateAPIView, ResponseController):
    http_method_names = ["patch"]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, (IsSuperAdmin | IsAdmin)]
    serializer_class = UpdateRegionSerializer

    @extend_schema(
        tags=["Regions"],
        summary="Update region",
        description="Updates an existing region. Only provided fields will be updated.",
        request=UpdateRegionSerializer,
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                description="Region updated successfully.",
                examples=[
                    OpenApiExample(
                        name="Success Example",
                        value={
                            "success": True,
                            "message": "Region updated successfully.",
                            "data": {
                                "id": 5,
                                "name_uz": "Toshkent",
                                "name_ru": "Ташкент",
                                "name_en": "Tashkent",
                                "name_uz_cyrl": "Тошкент",
                                "created_at": "2025-01-12T09:30:00Z",
                            },
                        },
                        status_codes=[200],
                    ),
                ],
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Region not found."
            ),
        },
    )
    def patch(self, request, *args, **kwargs):
        region_id = kwargs.get("pk")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = update_region(
            region_id=region_id,
            updated_by=request.user,
            **serializer.validated_data
        )

        return self.success_response(
            message=Message.REGION_UPDATED_SUCCESSFULLY,
            data=data,
            status=status.HTTP_200_OK
        )