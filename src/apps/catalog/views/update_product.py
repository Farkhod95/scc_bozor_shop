from rest_framework import status, serializers
from rest_framework.generics import UpdateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.catalog.services.update_product import update_product
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin, IsAdmin
from apps.core.services.docs import common_responses
from apps.core.services.model_status import UnitType
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message


class UpdateProductSerializer(serializers.Serializer):
    name_uz = serializers.CharField(required=False, allow_blank=True)
    name_ru = serializers.CharField(required=False, allow_blank=True)
    name_en = serializers.CharField(required=False, allow_blank=True)
    name_uz_cyrl = serializers.CharField(required=False, allow_blank=True)
    unit = serializers.ChoiceField(choices=UnitType, required=False, allow_null=True)
    category_id = serializers.IntegerField(required=False, allow_null=True)
    photo_id = serializers.IntegerField(required=False, allow_null=True)

class UpdateProductAPIView(UpdateAPIView, ResponseController):
    http_method_names = ["patch"]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, (IsSuperAdmin | IsAdmin)]
    serializer_class = UpdateProductSerializer

    @extend_schema(
        tags=["Products"],
        summary="Update product",
        description="Updates an existing product. Only provided fields will be updated.",
        request=UpdateProductSerializer,
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                description="Product updated successfully.",
                examples=[
                    OpenApiExample(
                        name="Success Example",
                        value={
                            "success": True,
                            "message": "Product updated successfully.",
                            "data": {
                                "id": 10,
                                "category": 1,
                                "name": "Updated Product",
                                "unit": "kg",
                                "photo": "file/mathematics.jpg",
                                "created_at": "2025-01-12T09:30:00Z",
                            },
                        },
                        status_codes=[200],
                    ),
                ],
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Product or Category not found."
            ),
        },
    )
    def patch(self, request, *args, **kwargs):
        product_id = kwargs.get("pk")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        data = update_product(
            product_id=product_id,
            updated_by=request.user,
            **serializer.validated_data,
        )

        return self.success_response(
            message=Message.PRODUCT_UPDATED_SUCCESSFULLY,
            data=data,
            status=status.HTTP_200_OK,
        )