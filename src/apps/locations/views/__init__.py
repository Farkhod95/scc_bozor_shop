from .create_city import CreateCityAPIView
from .delete_city import DeleteCityAPIView
from .detail_city import DetailCityAPIView
from .list_city import ListCityAPIView
from .update_city import UpdateCityAPIView

from .create_region import CreateRegionAPIView
from .delete_region import DeleteRegionAPIView
from .detail_region import DetailRegionAPIView
from .list_region import ListRegionAPIView
from .update_region import UpdateRegionAPIView

__all__ = [
    "CreateCityAPIView",
    "DeleteCityAPIView",
    "DetailCityAPIView",
    "ListCityAPIView",
    "UpdateCityAPIView",

    "CreateRegionAPIView",
    "DeleteRegionAPIView",
    "DetailRegionAPIView",
    "ListRegionAPIView",
    "UpdateRegionAPIView",
]