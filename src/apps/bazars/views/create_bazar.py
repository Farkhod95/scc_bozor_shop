from rest_framework import status, serializers
from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.bazars.services.create_bazar import create_bazar
from apps.core.services.response_controller import ResponseController
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin
from apps.core.services.docs import common_responses
from apps.core.services.responses import Message


class CreateBazarSerializer(serializers.Serializer):
    name_uz = serializers.CharField()
    name_ru = serializers.CharField(required=False)
    name_en = serializers.CharField(required=False)
    name_uz_cyrl = serializers.CharField(required=False)
    city_id = serializers.IntegerField()
    address = serializers.CharField()
    total_places = serializers.IntegerField()


class CreateBazarAPIView(CreateAPIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    serializer_class = CreateBazarSerializer

    @extend_schema(
        tags=["Bazars"],
        summary="Create Bazar",
        description="Create a new bazar using service layer.",
        responses={
            **common_responses,
            status.HTTP_201_CREATED: OpenApiResponse(description="Bazar created successfully."),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = create_bazar(**serializer.validated_data, user=request.user)

        return self.success_response(
            message=Message.BAZAR_CREATED_SUCCESSFULLY,
            data=data,
            status=status.HTTP_201_CREATED,
        )
