from rest_framework import serializers, status, permissions
from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsSuperAdmin, IsAuthenticated, IsAdmin
from apps.core.services.docs import common_responses
from apps.catalog.services.create_subcategory import create_subcategory
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message


class CreateSubcategorySerializer(serializers.Serializer):
    title_uz = serializers.CharField(max_length=255)
    title_ru = serializers.CharField(max_length=255, required=False, allow_blank=True)
    title_en = serializers.CharField(max_length=255, required=False, allow_blank=True)
    title_uz_cyrl = serializers.CharField(max_length=255, required=False, allow_blank=True)

    description_uz = serializers.CharField()
    description_ru = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    description_en = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    description_uz_cyrl = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    photo_id = serializers.IntegerField()


class CreateSubcategoryAPIView(CreateAPIView, ResponseController):
    serializer_class = CreateSubcategorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, (IsSuperAdmin | IsAdmin)]

    @extend_schema(
        tags=["Subcategories"],
        summary="Create a new subcategory",
        description="Create a new subcategory with a title and optional description.",
        request=CreateSubcategorySerializer,
        responses={
            **common_responses,
            status.HTTP_201_CREATED: OpenApiResponse(
                response=CreateSubcategorySerializer,
                description="Subcategory created successfully.",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "Subcategory created successfully.",
                            "data": {
                                "id": 1,
                                "title": "Mathematics",
                                "description": "All math related courses",
                                "photo": "file/mathematics.jpg",
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

        data = create_subcategory(
            **serializer.validated_data,
            created_by=request.user,
        )

        return self.success_response(
            message=Message.SUBCATEGORY_CREATED_SUCCESSFULLY,
            data=data,
            status=status.HTTP_201_CREATED
        )
