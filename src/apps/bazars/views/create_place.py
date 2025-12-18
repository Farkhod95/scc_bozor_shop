from rest_framework import status, serializers
from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsSuperAdmin, IsAuthenticated, IsBazarAdmin
from apps.core.services.docs import common_responses
from apps.bazars.services.create_place import create_places
from apps.core.services.response_controller import ResponseController
from apps.core.services.responses import Message


class CreatePlaceSerializer(serializers.Serializer):
    bazar_id = serializers.IntegerField()
    count = serializers.IntegerField(min_value=1, default=1, help_text="Number of places to create")


class CreatePlaceAPIView(CreateAPIView, ResponseController):
    serializer_class = CreatePlaceSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, (IsSuperAdmin | IsBazarAdmin)]

    @extend_schema(
        tags=["Places"],
        summary="Create Places for a Bazar",
        description="Automatically generate place numbers for a bazar and create them.",
        request=CreatePlaceSerializer,
        responses={
            **common_responses,
            status.HTTP_201_CREATED: OpenApiResponse(
                response=CreatePlaceSerializer,
                description="Places created successfully",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "Places created successfully",
                            "data": [
                                {"id": 1, "bazar_id": 1, "number": 1, "is_active": True},
                                {"id": 2, "bazar_id": 1, "number": 2, "is_active": True}
                            ]
                        }
                    )
                ]
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = create_places(
            user=request.user,
            **serializer.validated_data
        )

        return self.success_response(
            message=Message.PLACE_CREATED_SUCCESSFULLY,
            data=data,
            status=status.HTTP_201_CREATED
        )