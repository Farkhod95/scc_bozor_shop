from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.uploads.views import upload_file

app_name = "uploads"

router = DefaultRouter()


urlpatterns = [
    path("upload/file", upload_file.UploadFileView.as_view(), name="upload_file"),
] + router.urls