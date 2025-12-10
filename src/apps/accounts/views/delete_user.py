from rest_framework import status
from rest_framework.generics import GenericAPIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample

from apps.accounts.services.delete_user import delete_user
from apps.core.auth.permissions import IsAuthenticated, IsSuperAdmin
from apps.core.auth.authentication import JWTAuthentication
from apps.core.services.response_controller import ResponseController
from apps.core.services.docs import common_responses
from apps.core.services.responses import Message


class DeleteUserAPIView(GenericAPIView, ResponseController):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    @extend_schema(
        tags=["Users"],
        summary="Delete user",
        description="Delete a user by ID.",
        responses={
            **common_responses,
            status.HTTP_200_OK: OpenApiResponse(
                description="User deleted successfully.",
                examples=[
                    OpenApiExample(
                        name="Success",
                        value={"message": "User deleted successfully."},
                    ),
                ],
            ),
        },
    )
    def delete(self, request, *args, **kwargs):
        user_id = kwargs.get("pk")
        delete_user(user_id)

        return self.success_response(
            data=None,
            message=Message.USER_DELETED_SUCCESSFULLY,
            status=status.HTTP_200_OK,
        )
