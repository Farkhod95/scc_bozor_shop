from rest_framework import status, serializers
from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin, IsAdmin
from apps.core.services.docs import common_responses
from apps.locations.services.create_city import create_city
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message


class CreateCitySerializer(serializers.Serializer):
    name_uz = serializers.CharField(max_length=255)
    name_ru = serializers.CharField(max_length=255, required=False, allow_blank=True)
    name_en = serializers.CharField(max_length=255, required=False, allow_blank=True)
    name_uz_cyrl = serializers.CharField(max_length=255, required=False, allow_blank=True)
    code = serializers.CharField(max_length=10)
    region_id = serializers.IntegerField()


class CreateCityAPIView(CreateAPIView, ResponseController):
    serializer_class = CreateCitySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    @extend_schema(
        tags=["Cities"],
        summary="Create a new city",
        description="Create a new city with name, code and region.",
        request=CreateCitySerializer,
        responses={
            **common_responses,
            status.HTTP_201_CREATED: OpenApiResponse(
                response=CreateCitySerializer,
                description="City created successfully.",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "City created successfully.",
                            "data": {
                                "id": 5,
                                "name_uz": "Namangan",
                                "name_ru": "Наманган",
                                "name_en": "Namangan",
                                "name_uz_cyrl": "Наманган",
                                "code": "NM",
                                "region_id": 1,
                                "created_at": "2025-12-11T12:00:00Z"
                            }
                        }
                    )
                ],
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = create_city(
            created_by=request.user,
            **serializer.validated_data
        )

        return self.success_response(
            message=Message.CITY_CREATED_SUCCESSFULLY,
            data=data,
            status=status.HTTP_201_CREATED
        )