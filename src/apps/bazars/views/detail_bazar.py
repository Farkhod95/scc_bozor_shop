from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.bazars.services.detail_bazar import get_bazar_detail
from apps.core.auth.authentication import JWTAuthentication
from apps.core.services.response_controller import ResponseController
from apps.core.services.docs import common_responses


class DetailBazarAPIView(RetrieveAPIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = []

    @extend_schema(
        tags=["Bazars"],
        summary="Get bazar detail",
        description="Returns detailed information about a bazar by its ID.",
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                description="Bazar detail returned successfully."
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Bazar not found."
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
                        "description": "Fresh fruit bazar",
                        "address": "123 Market St",
                        "city_id": 2,
                        "city": "New York",
                        "region": "NY",
                        "total_places": 150,
                        "lat": 40.7128,
                        "lng": -74.0060,
                        "images": [
                            {
                                "id": 10,
                                "url": "http://example.com/images/bazar1.jpg",
                                "is_main": True
                            },
                            {
                                "id": 11,
                                "url": "http://example.com/images/bazar2.jpg",
                                "is_main": False
                            }
                        ],
                        "sections": [
                            {
                                "id": 1,
                                "name": "Section 1",
                                "svg": "http://example.com/media/section1.svg"
                            },
                        ],
                        "created_at": "2025-01-15T12:00:30Z"
                    }
                },
                status_codes=[200],
            ),
            OpenApiExample(
                name="Not Found",
                value={"detauk": "Bazar not found"},
                status_codes=[404],
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        bazar_id = kwargs.get("pk")

        data = get_bazar_detail(bazar_id=bazar_id, user=request.user, lang=request.lang)

        return self.success_response(
            data=data,
            status=status.HTTP_200_OK
        )
