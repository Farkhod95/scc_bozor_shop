from rest_framework import status, serializers
from rest_framework.generics import UpdateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.catalog.services.update_category import update_category
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin, IsAdmin, IsManager
from apps.core.services.docs import common_responses
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message


class UpdateCategorySerializer(serializers.Serializer):
    title_uz = serializers.CharField(max_length=255, required=False, allow_blank=True)
    title_ru = serializers.CharField(max_length=255, required=False, allow_blank=True)
    title_en = serializers.CharField(max_length=255, required=False, allow_blank=True)
    title_uz_cyrl = serializers.CharField(max_length=255, required=False, allow_blank=True)

    description_uz = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    description_ru = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    description_en = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    description_uz_cyrl = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    photo_id = serializers.IntegerField(required=False, allow_null=True)


class UpdateCategoryAPIView(UpdateAPIView, ResponseController):
    http_method_names = ["patch"]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, (IsSuperAdmin | IsManager | IsAdmin)]
    serializer_class = UpdateCategorySerializer

    @extend_schema(
        tags=["Categories"],
        summary="Update category",
        description="Updates an existing category. Only provided fields will be updated.",
        request=UpdateCategorySerializer,
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                description="Category updated successfully.",
                examples=[
                    OpenApiExample(
                        name="Success Example",
                        value={
                            "success": True,
                            "message": "Category updated successfully.",
                            "data": {
                                "id": 1,
                                "title_uz": "Updated Category",
                                "title_ru": "Обновленная категория",
                                "title_en": "Updated Category",
                                "title_uz_cyrl": "Янгиланган категория",
                                "description_uz": "Updated description",
                                "description_ru": "Обновленное описание",
                                "description_en": "Updated description",
                                "description_uz_cyrl": "Янгиланган тавсиф",
                                "photo": "file/mathematics.jpg",
                                "created_at": "2025-01-01T12:00:00Z",
                            },
                        },
                        status_codes=[200],
                    )
                ],
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Category not found."
            ),
        },
    )
    def patch(self, request, *args, **kwargs):
        category_id = kwargs.get("pk")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = update_category(
            category_id=category_id,
            updated_by=request.user,
            **serializer.validated_data,
        )

        return self.success_response(
            message=Message.CATEGORY_UPDATED_SUCCESSFULLY,
            data=data,
            status=status.HTTP_200_OK,
        )
