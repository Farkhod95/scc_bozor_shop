from rest_framework import status
from rest_framework.generics import DestroyAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.catalog.services.delete_category import delete_category
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin, IsAdmin
from apps.core.services.response_controller import ResponseController
from apps.core.services.docs import common_responses
from apps.core.services.responses import Message


class DeleteCategoryAPIView(DestroyAPIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, (IsSuperAdmin | IsAdmin)]

    @extend_schema(
        tags=["Categories"],
        summary="Delete category",
        description="Delete category by ID. Only SuperAdmin can delete categories.",
        responses={
            **common_responses,
            status.HTTP_204_NO_CONTENT: OpenApiResponse(
                description="Category deleted successfully.",
                examples=[
                    OpenApiExample(
                        "Not Found Example",
                        value={"detail": "Category not found"},
                        status_codes=[404],
                    )
                ]
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Category not found."
            ),
        }
    )
    def delete(self, request, *args, **kwargs):
        category_id = kwargs.get("pk")
        delete_category(category_id)
        return self.success_response(
            message=Message.CATEGORY_DELETED_SUCCESSFULLY,
            status=status.HTTP_200_OK
        )
