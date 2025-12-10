from .create_category import CreateCategoryAPIView
from .list_category import ListCategoryAPIView
from .delete_category import DeleteCategoryAPIView
from .detail_category import DetailCategoryAPIView
from .update_category import UpdateCategoryAPIView

from .create_product import CreateProductAPIView
from .list_product import ListProductAPIView
from .delete_product import DeleteProductAPIView
from .detail_product import DetailProductAPIView
from .update_product import UpdateProductAPIView


__all__ = [
    "CreateCategoryAPIView",
    "ListCategoryAPIView",
    "DeleteCategoryAPIView",
    "DetailCategoryAPIView",
    "UpdateCategoryAPIView",

    "CreateProductAPIView",
    "ListProductAPIView",
    "DeleteProductAPIView",
    "DetailProductAPIView",
    "UpdateProductAPIView",
]

