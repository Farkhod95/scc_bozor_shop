from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.locations.services.detail_region import get_region_detail
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated
from apps.core.services.response_controller import ResponseController
from apps.core.services.docs import common_responses


class DetailRegionAPIView(RetrieveAPIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Regions"],
        summary="Get region detail",
        description="Returns detailed information about a region by its ID.",
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                description="Region detail returned successfully.",
                examples=[
                    OpenApiExample(
                        name="Success Example",
                        value={
                            "success": True,
                            "data": {
                                "id": 1,
                                "name_uz": "Farg‘ona",
                                "name_ru": "Фергана",
                                "name_en": "Fergana",
                                "name_uz_cyrl": "Фарғона",
                                "created_at": "2025-01-15T12:00:30Z",
                            }
                        },
                        status_codes=[200],
                    )
                ],
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Region not found."
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        region_id = kwargs.get("pk")

        data = get_region_detail(
            region_id=region_id,
            user=request.user,
            lang=request.lang
        )

        return self.success_response(
            data=data,
            status=status.HTTP_200_OK
        )
