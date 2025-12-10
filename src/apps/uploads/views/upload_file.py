from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from apps.uploads.services.upload_file import create_file


class UploadFileSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)


class UploadedFileDataSerializer(serializers.Serializer):
    file = serializers.CharField()


class UploadedFileResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = UploadedFileDataSerializer()


class ErrorResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()


class UploadFileView(APIView):
    @extend_schema(
        request=UploadFileSerializer,
        responses={
            201: OpenApiResponse(
                response=UploadedFileResponseSerializer,
                description="File successfully uploaded."
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Validation error or bad request."
            ),
        },
        description=(
                "Uploads a file with optional user information.\n\n"
                "- `file` is required and must be a valid file.\n"
                "- `user` is optional.\n"
                "- Returns uploaded file path inside `data.file`."
        ),
        summary="Upload a file",
        operation_id="upload_file",
        tags=["Upload"],
        examples=[
            OpenApiExample(
                name="Upload Response",
                value={
                    "message": "Successfully created.",
                    "data": {
                        "file": "/media/files/5b86259f-7cdf-47cd-9538-5d535c28cbb2.png"
                    }
                },
                response_only=True,
                status_codes=["201"]
            ),
        ]
    )
    def post(self, request):
        serializer = UploadFileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = create_file(**serializer.validated_data)
        return Response({"message": "Successfully created.", "data": data}, status=status.HTTP_201_CREATED)