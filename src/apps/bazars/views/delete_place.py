from rest_framework import status
from rest_framework.generics import DestroyAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin, IsBazarAdmin, IsManager
from apps.core.services.docs import common_responses
from apps.bazars.services.delete_place import delete_place
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message


class DeletePlaceAPIView(DestroyAPIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, (IsSuperAdmin | IsBazarAdmin | IsManager)]
    lookup_url_kwarg = "place_id"

    @extend_schema(
        tags=["Places"],
        summary="Delete a Place",
        description="Delete a specific Place by ID and update the Bazar's total_places.",
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                description="Place deleted successfully",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "Place deleted successfully",
                            "data": None
                        }
                    )
                ]
            ),
        },
    )
    def delete(self, request, *args, **kwargs):
        place_id = kwargs.get(self.lookup_url_kwarg)
        delete_place(request.user, place_id=int(place_id))
        return self.success_response(
            message=Message.PLACE_DELETED_SUCCESSFULLY,
            status=status.HTTP_200_OK
        )
