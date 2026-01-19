from rest_framework import serializers, status, permissions
from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.catalog.services.create_product import create_product
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsSuperAdmin, IsAuthenticated, IsAdmin, IsManager
from apps.core.services.response_controller import ResponseController
from apps.core.services.docs import common_responses
from apps.core.services.responses import Message
from apps.core.services.model_status import UnitType


class CreateProductSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    subcategory_id = serializers.IntegerField(required=False)

    name_uz = serializers.CharField(max_length=255)
    name_ru = serializers.CharField(max_length=255, required=False, allow_blank=True)
    name_en = serializers.CharField(max_length=255, required=False, allow_blank=True)
    name_uz_cyrl = serializers.CharField(max_length=255, required=False, allow_blank=True)

    unit = serializers.ChoiceField(choices=UnitType)
    photo_id = serializers.IntegerField()


class CreateProductAPIView(CreateAPIView, ResponseController):
    serializer_class = CreateProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, (IsSuperAdmin | IsManager | IsAdmin)]

    @extend_schema(
        tags=["Products"],
        summary="Create a new product",
        description="Create a new product under a specific category. Only superadmins can create products.",
        request=CreateProductSerializer,
        responses={
            **common_responses,
            status.HTTP_201_CREATED: OpenApiResponse(
                response=CreateProductSerializer,
                description="Product created successfully.",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "Product created successfully.",
                            "data": {
                                "id": 1,
                                "category": 3,
                                "subcategory": 2,
                                "name": "Laptop",
                                "unit": "pcs",
                                "photo": "file/mathematics.jpg",
                                "created_at": "2025-12-05T10:30:00Z"
                            }
                        }
                    ),
                ]
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                description="Invalid input data or category not found.",
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = create_product(
            created_by=request.user,
            **serializer.validated_data
        )

        return self.success_response(
            message=Message.PRODUCT_CREATED_SUCCESSFULLY,
            data=data,
            status=status.HTTP_201_CREATED
        )
