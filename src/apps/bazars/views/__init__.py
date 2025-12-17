from .list_bazar import ListBazarAPIView
from .create_bazar import CreateBazarAPIView
from .delete_bazar import DeleteBazarAPIView
from .update_bazar import UpdateBazarView
from .detail_bazar import DetailBazarAPIView

from .create_bazar_admin import CreateBazarAdminAPIView
from .list_bazar_admin import ListBazarAdminAPIView
from .detail_bazar_admin import DetailBazarAdminAPIView
from .delete_bazar_admin import DeleteBazarAdminAPIView
from .update_bazar_admin import UpdateBazarAdminAPIView

from .create_place import CreatePlaceAPIView
from .list_place import ListPlaceAPIView
from .detail_place import DetailPlaceAPIView
from .delete_place import DeletePlaceAPIView

from .create_qrcode import CreateQRCodeAPIView
from .update_qrcode import UpdateQRCodeAPIView
from .get_place_by_qr import GetPlaceByQRAPIView

from .create_place_product import CreatePlaceProductAPIView
from .update_place_product import UpdatePlaceProductAPIView
from .list_place_product import ListPlaceProductAPIView
from .delete_place_product import DeletePlaceProductAPIView

from .create_bazar_image import CreateBazarImageAPIView
from .delete_bazar_image import DeleteBazarImageAPIView
from .list_bazar_images import ListBazarImageAPIView
from .update_bazar_image import UpdateBazarImageAPIView


__all__ = [
    "ListBazarAPIView",
    "CreateBazarAPIView",
    "DeleteBazarAPIView",
    "UpdateBazarView",
    "DetailBazarAPIView",

    "CreateBazarAdminAPIView",
    "ListBazarAdminAPIView",
    "DetailBazarAdminAPIView",
    "DeleteBazarAdminAPIView",
    "UpdateBazarAdminAPIView",

    "CreatePlaceAPIView",
    "ListPlaceAPIView",
    "DetailPlaceAPIView",
    "DeletePlaceAPIView",

    "CreateQRCodeAPIView",
    "UpdateQRCodeAPIView",
    "GetPlaceByQRAPIView",

    "CreatePlaceProductAPIView",
    "UpdatePlaceProductAPIView",
    "ListPlaceProductAPIView",
    "DeletePlaceProductAPIView",

    "CreateBazarImageAPIView",
    "DeleteBazarImageAPIView",
    "ListBazarImageAPIView",
    "UpdateBazarImageAPIView",
]