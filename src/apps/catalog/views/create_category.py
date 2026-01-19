from rest_framework import serializers, status, permissions
from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsSuperAdmin, IsAuthenticated, IsAdmin, IsManager
from apps.core.services.docs import common_responses
from apps.catalog.services.create_category import create_category
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message


class CreateCategorySerializer(serializers.Serializer):
    title_uz = serializers.CharField(max_length=255)
    title_ru = serializers.CharField(max_length=255, required=False, allow_blank=True)
    title_en = serializers.CharField(max_length=255, required=False, allow_blank=True)
    title_uz_cyrl = serializers.CharField(max_length=255, required=False, allow_blank=True)

    description_uz = serializers.CharField()
    description_ru = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    description_en = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    description_uz_cyrl = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    photo_id = serializers.IntegerField()


class CreateCategoryAPIView(CreateAPIView, ResponseController):
    serializer_class = CreateCategorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, (IsSuperAdmin | IsManager | IsAdmin)]

    @extend_schema(
        tags=["Categories"],
        summary="Create a new category",
        description="Create a new category with a title and optional description.",
        request=CreateCategorySerializer,
        responses={
            **common_responses,
            status.HTTP_201_CREATED: OpenApiResponse(
                response=CreateCategorySerializer,
                description="Category created successfully.",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "Category created successfully.",
                            "data": {
                                "id": 1,
                                "title": "Mathematics",
                                "photo": "file/mathematics.jpg",
                                "description": "All math related courses",
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

        data = create_category(
            **serializer.validated_data,
            created_by=request.user,
        )

        return self.success_response(
            message=Message.CATEGORY_CREATED_SUCCESSFULLY,
            data=data,
            status=status.HTTP_201_CREATED
        )
