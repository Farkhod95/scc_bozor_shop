from rest_framework import status, serializers
from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin
from apps.core.services.docs import common_responses
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message
from apps.bazars.services.create_bazar_image import create_bazar_image


class CreateBazarImageSerializer(serializers.Serializer):
    bazar_id = serializers.IntegerField()
    image_id = serializers.IntegerField()
    is_main = serializers.BooleanField(default=False)


class CreateBazarImageAPIView(CreateAPIView, ResponseController):
    serializer_class = CreateBazarImageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    @extend_schema(
        tags=["Bazar Images"],
        summary="Create bazar image",
        description="Attach an uploaded file as an image to a bazar.",
        request=CreateBazarImageSerializer,
        responses={
            **common_responses,
            status.HTTP_201_CREATED: OpenApiResponse(
                response=CreateBazarImageSerializer,
                description="Bazar image created successfully.",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "Bazar image created successfully.",
                            "data": {
                                "id": 1,
                                "bazar_id": 3,
                                "image": "/media/uploads/example.jpg",
                                "is_main": True,
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

        data = create_bazar_image(
            **serializer.validated_data
        )

        return self.success_response(
            message=Message.BAZAR_IMAGE_CREATED_SUCCESSFULLY,
            data=data,
            status=status.HTTP_201_CREATED
        )
