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
                description="Bazar detail returned successfully.",
                examples=[
                    OpenApiExample(
                        name="Success Example",
                        value={
                            "message": "OK",
                            "data": {
                                "id": 1,
                                "name": "Markaziy Bozor",
                                "address": "Mustaqillik ko'chasi 1",
                                "city_id": 2,
                                "city": "Toshkent",
                                "region": "Toshkent viloyati",
                                "total_places": 150,
                                "average_rating": 4.5,
                                "review_count": 20,
                                "lat": 41.2995,
                                "lng": 69.2401,
                                "images": [
                                    {
                                        "id": 10,
                                        "url": "http://example.com/media/images/bazar1.jpg",
                                        "is_main": True
                                    },
                                    {
                                        "id": 11,
                                        "url": "http://example.com/media/images/bazar2.jpg",
                                        "is_main": False
                                    }
                                ],
                                "sections": [
                                    {
                                        "id": 1,
                                        "name": "A sektor",
                                        "svg": "http://example.com/media/sections/a-sektor.svg"
                                    }
                                ],
                                "created_at": "2025-01-15T12:00:30Z"
                            }
                        },
                        status_codes=["200"],
                    )
                ]
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Bazar not found.",
                examples=[
                    OpenApiExample(
                        name="Not Found",
                        value={"detail": "Bazar not found"},
                        status_codes=["404"],
                    )
                ]
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        bazar_id = kwargs.get("pk")

        data = get_bazar_detail(bazar_id=bazar_id, user=request.user, lang=request.lang)

        return self.success_response(
            data=data,
            status=status.HTTP_200_OK
        )
