from rest_framework import status
from drf_spectacular.utils import OpenApiResponse, OpenApiExample
from apps.core.serializers import ErrorResponseSerializer


common_responses = {
    status.HTTP_400_BAD_REQUEST: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Bad request",
        examples=[
            OpenApiExample(
                "Invalid Data",
                summary="The request payload is invalid or missing required fields",
                value={
                    "detail": "Invalid Data"
                },
            )
        ]
    ),

    status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Authentication failed",
        examples=[
            OpenApiExample(
                "Unauthorized",
                summary="User failed to authenticate",
                value={
                    "detail": "Authentication credentials were not provided."
                },
            )
        ]
    ),

    status.HTTP_403_FORBIDDEN: OpenApiResponse(
        response=ErrorResponseSerializer,
        description="Permission denied",
        examples=[
            OpenApiExample(
                "Access Denied",
                summary="User does not have permission",
                value={
                    "detail": "You do not have permission to perform this action."
                },
            )
        ]
    ),

}