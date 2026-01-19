from rest_framework import status, serializers
from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsSuperAdmin, IsAuthenticated, IsAdmin, IsManager
from apps.core.services.docs import common_responses
from apps.bazars.services.create_bazar_admin import create_bazar_admin
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message


class CreateBazarAdminSerializer(serializers.Serializer):
    bazar_id = serializers.IntegerField()
    user_id = serializers.IntegerField()


class CreateBazarAdminAPIView(CreateAPIView, ResponseController):
    serializer_class = CreateBazarAdminSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, (IsSuperAdmin | IsManager)]

    @extend_schema(
        tags=["Bazar Admins"],
        summary="Assign user as Bazar Admin",
        description="Assign a user as an admin for a specific bazar.",
        request=CreateBazarAdminSerializer,
        responses={
            **common_responses,
            status.HTTP_201_CREATED: OpenApiResponse(
                response=CreateBazarAdminSerializer,
                description="Bazar admin created successfully.",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "Bazar admin created successfully.",
                            "data": {
                                "id": 1,
                                "bazar_id": 1,
                                "user_id": 2,
                                "assigned_at": "2025-12-12T10:00:00Z",
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

        data = create_bazar_admin(
            **serializer.validated_data
        )

        return self.success_response(
            message=Message.BAZAR_ADMIN_CREATED_SUCCESSFULLY,
            data=data,
            status=status.HTTP_201_CREATED
        )
