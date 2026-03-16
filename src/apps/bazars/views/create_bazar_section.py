from rest_framework import status, serializers
from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from apps.bazars.services.create_bazar_section import create_bazar_section
from apps.core.services.response_controller import ResponseController
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin
from apps.core.services.docs import common_responses
from apps.core.services.responses import Message

class CreateBazarSectionSerializer(serializers.Serializer):
    bazar_id = serializers.IntegerField()
    file = serializers.FileField()
    name = serializers.CharField()


class CreateBazarSectionAPIView(CreateAPIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    serializer_class = CreateBazarSectionSerializer

    @extend_schema(
        tags=["Bazar Sections"],
        summary="Create Bazar Section",
        description="Create a new bazar section using service layer.",
        responses={
            **common_responses,
            status.HTTP_201_CREATED: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Bazar section created successfully.",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "Bazar section created successfully.",
                            "data": {
                                "id": 1,
                                "bazar_id": 3,
                                "name": "A sektor",
                                "svg": "http://example.com/media/sections/a-sektor.svg",
                                "created_at": "2025-01-15T12:00:00Z"
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

        data = create_bazar_section(**serializer.validated_data, user=request.user)

        return self.success_response(
            message=Message.BAZAR_SECTION_CREATED_SUCCESSFULLY,
            data=data,
            status=status.HTTP_201_CREATED,
        )
