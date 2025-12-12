from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.locations.services.detail_city import get_city_detail
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated
from apps.core.services.response_controller import ResponseController
from apps.core.services.docs import common_responses


class DetailCityAPIView(RetrieveAPIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Cities"],
        summary="Get city detail",
        description="Returns detailed information about a city by its ID.",
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                description="City detail returned successfully."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="City not found."
            ),
        },
        examples=[
            OpenApiExample(
                name="Success Example",
                value={
                    "success": True,
                    "data": {
                        "id": 5,
                        "name": "Namangan",
                        "code": "NM",
                        "region_id": 1,
                        "created_at": "2025-12-11T12:00:00Z"
                    }
                },
                status_codes=[200],
            ),
            OpenApiExample(
                name="Not Found",
                value={"detail": "City not found"},
                status_codes=[404],
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        city_id = kwargs.get("pk")

        data = get_city_detail(city_id=city_id, user=request.user, lang=request.lang)

        return self.success_response(
            data=data,
            status=status.HTTP_200_OK
        )
