from rest_framework import status, serializers
from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse

from apps.bazars.services.list_bazar import list_bazar
from apps.core.services.response_controller import ResponseController
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated
from apps.core.services.docs import common_responses


class ListBazarQuerySerializer(serializers.Serializer):
    city_id = serializers.IntegerField(required=False)


class ListBazarItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    city = serializers.CharField()
    region = serializers.CharField()
    address = serializers.CharField()
    total_places = serializers.IntegerField()


class ListBazarAPIView(ListAPIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        tags=["Bazar"],
        summary="List bazars",
        description="Return a list of bazars with optional city filter.",
        parameters=[ListBazarQuerySerializer],
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                response=ListBazarItemSerializer(many=True),
                description="Successful response with bazar list.",
            ),
        },
    )
    def get(self, request, *args, **kwargs):
        serializer = ListBazarQuerySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        data = list_bazar(**serializer.validated_data)

        return self.success_response(
            data=data,
            status=status.HTTP_200_OK,
        )
