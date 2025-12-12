from django.urls import path
from apps.bazars.views import *

app_name = "catalog"

urlpatterns = [
    # Bazars
    path("bazar/list/", ListBazarAPIView.as_view(), name="list-bazars"),
    path("bazar/create/", CreateBazarAPIView.as_view(), name="create-bazar"),
    path("bazar/<int:pk>/detail/", DetailBazarAPIView.as_view(), name="detail-bazar"),
    path("bazar/<int:pk>/update/", UpdateBazarView.as_view(), name="update-bazar"),
    path("bazar/<int:pk>/delete/", DeleteBazarAPIView.as_view(), name="delete-bazar"),

    # Bazar Admins
    path("bazar-admin/create/", CreateBazarAdminAPIView.as_view(), name="create-bazar-admin"),
    path("bazar-admin/list/", ListBazarAdminAPIView.as_view(), name="list-bazar-admins"),
    path("bazar-admin/<int:pk>/detail/", DetailBazarAdminAPIView.as_view(), name="detail-bazar-admin"),
    path("bazar-admin/<int:pk>/delete/", DeleteBazarAdminAPIView.as_view(), name="delete-bazar-admin"),
    path("bazar-admin/<int:pk>/update/", UpdateBazarAdminAPIView.as_view(), name="update-bazar-admin"),
]