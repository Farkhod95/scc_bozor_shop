from rest_framework import serializers, status, permissions
from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.catalog.services.create_product import create_product
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsSuperAdmin, IsAuthenticated, IsAdmin
from apps.core.services.response_controller import ResponseController
from apps.core.services.docs import common_responses
from apps.core.services.responses import Message
from apps.core.services.model_status import UnitType


class CreateProductSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    unit = serializers.ChoiceField(choices=UnitType)

class CreateProductAPIView(CreateAPIView, ResponseController):
    serializer_class = CreateProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, (IsSuperAdmin | IsAdmin)]

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
                                "name": "Laptop",
                                "unit": "pcs",
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
            category_id=serializer.validated_data['category_id'],
            name=serializer.validated_data['name'],
            unit=serializer.validated_data['unit'],
            created_by=request.user
        )

        return self.success_response(
            message=Message.PRODUCT_CREATED_SUCCESSFULLY,
            data=data,
            status=status.HTTP_201_CREATED
        )
