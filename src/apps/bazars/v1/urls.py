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

    # Places
    path("place/create/", CreatePlaceAPIView.as_view(), name="create-place"),
    path("place/list/", ListPlaceAPIView.as_view(), name="list-places"),
    path("place/<int:pk>/detail/", DetailPlaceAPIView.as_view(), name="detail-place"),
    path("place/<int:place_id>/delete/", DeletePlaceAPIView.as_view(), name="delete-place"),
    path("place/by-qr/", GetPlaceByQRAPIView.as_view(), name="get-place-by-qr"),


    # QR Codes
    path("qrcode/create/", CreateQRCodeAPIView.as_view(), name="create-qrcode"),
    path("qrcode/<int:pk>/update/", UpdateQRCodeAPIView.as_view(), name="update-qrcode"),

    # Place Products
    path("place-product/create/", CreatePlaceProductAPIView.as_view(), name="create-place-product"),
    path("place-product/<int:pk>/update/", UpdatePlaceProductAPIView.as_view(), name="update-place-product"),
    path("place-product/list/", ListPlaceProductAPIView.as_view(), name="list-place-products"),
    path("place-product/<int:pk>/delete/", DeletePlaceProductAPIView.as_view(), name="delete-place-product"),
]