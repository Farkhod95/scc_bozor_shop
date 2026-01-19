from rest_framework import status, serializers
from rest_framework.generics import UpdateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.catalog.services.update_subcategory import update_subcategory
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin, IsAdmin, IsManager
from apps.core.services.docs import common_responses
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message


class UpdateSubcategorySerializer(serializers.Serializer):
    title_uz = serializers.CharField(max_length=255, required=False, allow_blank=True)
    title_ru = serializers.CharField(max_length=255, required=False, allow_blank=True)
    title_en = serializers.CharField(max_length=255, required=False, allow_blank=True)
    title_uz_cyrl = serializers.CharField(max_length=255, required=False, allow_blank=True)

    description_uz = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    description_ru = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    description_en = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    description_uz_cyrl = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    photo_id = serializers.IntegerField(required=False, allow_null=True)
    category_id = serializers.IntegerField(required=False, allow_null=True)


class UpdateSubcategoryAPIView(UpdateAPIView, ResponseController):
    http_method_names = ["patch"]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, (IsSuperAdmin | IsManager | IsAdmin)]
    serializer_class = UpdateSubcategorySerializer

    @extend_schema(
        tags=["Subcategories"],
        summary="Update subcategory",
        description="Updates an existing subcategory. Only provided fields will be updated.",
        request=UpdateSubcategorySerializer,
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                description="Subcategory updated successfully.",
                examples=[
                    OpenApiExample(
                        name="Success Example",
                        value={
                            "success": True,
                            "message": "Subcategory updated successfully.",
                            "data": {
                                "id": 1,
                                "title_uz": "Updated Subcategory",
                                "title_ru": "Обновленная категория",
                                "title_en": "Updated Subcategory",
                                "title_uz_cyrl": "Янгиланган категория",
                                "description_uz": "Updated description",
                                "description_ru": "Обновленное описание",
                                "description_en": "Updated description",
                                "description_uz_cyrl": "Янгиланган тавсиф",
                                "photo": "file/mathematics.jpg",
                                "category": 1,
                                "created_at": "2025-01-01T12:00:00Z",
                            },
                        },
                        status_codes=[200],
                    )
                ],
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Subcategory not found."
            ),
        },
    )
    def patch(self, request, *args, **kwargs):
        subcategory_id = kwargs.get("pk")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = update_subcategory(
            subcategory_id=subcategory_id,
            updated_by=request.user,
            **serializer.validated_data,
        )

        return self.success_response(
            message=Message.SUBCATEGORY_UPDATED_SUCCESSFULLY,
            data=data,
            status=status.HTTP_200_OK,
        )
