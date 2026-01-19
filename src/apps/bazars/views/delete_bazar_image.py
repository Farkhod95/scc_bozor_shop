from rest_framework import status
from rest_framework.generics import DestroyAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin, IsManager
from apps.core.services.docs import common_responses
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message
from apps.bazars.services.delete_bazar_image import delete_bazar_image


class DeleteBazarImageAPIView(DestroyAPIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, (IsSuperAdmin | IsManager)]

    @extend_schema(
        tags=["Bazar Images"],
        summary="Delete bazar image",
        description="Delete an image from a bazar. If the main image is deleted, another image is automatically set as main.",
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                description="Bazar image deleted successfully.",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "Bazar image deleted successfully.",
                        }
                    )
                ]
            ),
        },
    )
    def delete(self, request, *args, **kwargs):
        image_id = kwargs.get("image_id")

        delete_bazar_image(image_id=image_id)
        return self.success_response(
            message=Message.BAZAR_IMAGE_DELETED_SUCCESSFULLY,
            status=status.HTTP_200_OK
        )
