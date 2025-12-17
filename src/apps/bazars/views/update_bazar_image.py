from rest_framework import status, serializers
from rest_framework.generics import UpdateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin
from apps.core.services.docs import common_responses
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message
from apps.bazars.services.update_bazar_image import update_bazar_image


class UpdateBazarImageSerializer(serializers.Serializer):
    image_file_id = serializers.IntegerField(required=False)
    is_main = serializers.BooleanField(required=False)


class UpdateBazarImageAPIView(UpdateAPIView, ResponseController):
    serializer_class = UpdateBazarImageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    http_method_names = ["patch"]

    @extend_schema(
        tags=["Bazar Images"],
        summary="Update bazar image",
        description="Update image file or mark/unmark as main image.",
        request=UpdateBazarImageSerializer,
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                description="Bazar image updated successfully.",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "Bazar image updated successfully.",
                            "data": {
                                "id": 1,
                                "bazar_id": 3,
                                "image": "/media/uploads/new_image.jpg",
                                "is_main": True
                            }
                        }
                    )
                ]
            ),
        },
    )
    def patch(self, request, *args, **kwargs):
        image_id = kwargs.get("image_id")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = update_bazar_image(
            image_id=image_id,
            **serializer.validated_data
        )

        return self.success_response(
            message=Message.BAZAR_IMAGE_UPDATED_SUCCESSFULLY,
            data=data,
            status=status.HTTP_200_OK
        )
