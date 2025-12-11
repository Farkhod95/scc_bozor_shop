from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.catalog.services.detail_category import get_category_detail
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin, IsAdmin
from apps.core.services.response_controller import ResponseController
from apps.core.services.docs import common_responses


class DetailCategoryAPIView(RetrieveAPIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Categories"],
        summary="Get category detail",
        description="Returns detailed information about a category by its ID.",
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                description="Category detail returned successfully."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Category not found."
            ),
        },
        examples=[
            OpenApiExample(
                name="Success Example",
                value={
                    "success": True,
                    "data": {
                        "id": 1,
                        "title": "Fruits",
                        "description": "Fresh fruit category",
                        "created_at": "2025-01-15T12:00:30Z"
                    }
                },
                status_codes=[200],
            ),
            OpenApiExample(
                name="Not Found",
                value={"message_key": "category_not_found"},
                status_codes=[404],
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        category_id = kwargs.get("pk")

        data = get_category_detail(category_id=category_id, user=request.user, lang=request.lang)

        return self.success_response(
            data=data,
            status=status.HTTP_200_OK
        )
