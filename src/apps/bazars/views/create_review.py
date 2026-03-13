from rest_framework import status
from rest_framework.generics import CreateAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from rest_framework import serializers

from apps.bazars.services.create_review import create_review
from apps.core.services.response_controller import ResponseController
from apps.core.auth.authentication import JWTAuthentication
from apps.core.auth.permissions import IsAuthenticated
from apps.core.services.docs import common_responses
from apps.core.services.responses import Message


class CreateReviewSerializer(serializers.Serializer):
    bazar_id = serializers.IntegerField()
    rating = serializers.IntegerField(min_value=1, max_value=5)
    comment = serializers.CharField(required=False, allow_blank=True)


class CreateReviewAPIView(CreateAPIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CreateReviewSerializer

    @extend_schema(
        tags=["Reviews"],
        summary="Create Bazar Review",
        description="Rate a bazar and leave a comment.",
        responses={
            **common_responses,
            status.HTTP_201_CREATED: OpenApiResponse(
                description="Review created successfully.",
                examples=[
                    OpenApiExample(
                        "Success Example",
                        value={
                            "message": "Review created successfully.",
                            "data": {
                                "id": 1,
                                "bazar_id": 3,
                                "user_id": 12,
                                "rating": 5,
                                "comment": "Juda yaxshi bozor!",
                                "created_at": "2025-01-15T12:00:00Z"
                            }
                        }
                    )
                ]
            ),
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = create_review(
            user=request.user,
            **serializer.validated_data
        )

        return self.success_response(
            message=Message.REVIEW_CREATED,
            data=data,
            status=status.HTTP_201_CREATED,
        )