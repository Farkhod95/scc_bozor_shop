from rest_framework import status, serializers
from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.locations.services.create_region import create_region
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin
from apps.core.services.response_controller import ResponseController
from apps.core.services.docs import common_responses
from apps.core.services.responses import Message


class CreateRegionSerializer(serializers.Serializer):
    name_uz = serializers.CharField(max_length=255)
    name_ru = serializers.CharField(max_length=255, required=False, allow_blank=True)
    name_en = serializers.CharField(max_length=255, required=False, allow_blank=True)
    name_uz_cyrl = serializers.CharField(max_length=255, required=False, allow_blank=True)
    code = serializers.CharField(max_length=10)


class CreateRegionAPIView(CreateAPIView, ResponseController):
    serializer_class = CreateRegionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    @extend_schema(
        tags=["Regions"],
        summary="Create a new region",
        description="Create a new region with names in multiple languages. Only superadmins or admins can create regions.",
        request=CreateRegionSerializer,
        responses={
            **common_responses,
            status.HTTP_201_CREATED: OpenApiResponse(
                response=CreateRegionSerializer,
                description="Region created successfully.",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "Region created successfully.",
                            "data": {
                                "id": 1,
                                "name_uz": "Namangan",
                                "name_ru": "Наманган",
                                "name_en": "Namangan",
                                "name_uz_cyrl": "Наманган",
                                "created_at": "2025-12-11T12:00:00Z"
                            }
                        }
                    )
                ]
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid input data.",
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = create_region(
            created_by=request.user,
            **serializer.validated_data
        )

        return self.success_response(
            message=Message.REGION_CREATED_SUCCESSFULLY,
            data=data,
            status=status.HTTP_201_CREATED
        )
