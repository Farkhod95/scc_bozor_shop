from django.urls import path
from apps.catalog.views import *

app_name = "catalog"

urlpatterns = [
    # Categories
    path("category/list/", ListCategoryAPIView.as_view(), name="list-category"),
    path("category/create/", CreateCategoryAPIView.as_view(), name="create-category"),
    path("category/<int:pk>/detail/", DetailCategoryAPIView.as_view(), name="detail-category"),
    path("category/<int:pk>/update/", UpdateCategoryAPIView.as_view(), name="update-category"),
    path("category/<int:pk>/delete/", DeleteCategoryAPIView.as_view(), name="delete-category"),

    # Subcategories
    path("subcategory/list/", ListSubcategoryAPIView.as_view(), name="list-subcategory"),
    path("subcategory/create/", CreateSubcategoryAPIView.as_view(), name="create-subcategory"),
    path("subcategory/<int:pk>/detail/", DetailSubcategoryAPIView.as_view(), name="detail-subcategory"),
    path("subcategory/<int:pk>/update/", UpdateSubcategoryAPIView.as_view(), name="update-subcategory"),
    path("subcategory/<int:pk>/delete/", DeleteSubcategoryAPIView.as_view(), name="delete-subcategory"),

    # Products
    path("product/list/", ListProductAPIView.as_view(), name="list-products"),
    path("product/create/", CreateProductAPIView.as_view(), name="create-product"),
    path("product/<int:pk>/detail/", DetailProductAPIView.as_view(), name="product-detail"),
    path("product/<int:pk>/update/", UpdateProductAPIView.as_view(), name="update-product"),
    path("product/<int:pk>/delete/", DeleteProductAPIView.as_view(), name="delete-product"),
]
