from django.urls import path
from apps.catalog.views import *

app_name = "catalog"

urlpatterns = [
    # Categories
    path("category/list/", ListCategoryAPIView.as_view(), name="list-categories"),
    path("category/create/", CreateCategoryAPIView.as_view(), name="create-category"),
    path("category/<int:pk>/detail/", DetailCategoryAPIView.as_view(), name="category-detail"),
    path("category/<int:pk>/update/", UpdateCategoryAPIView.as_view(), name="update-category"),
    path("category/<int:pk>/delete/", DeleteCategoryAPIView.as_view(), name="delete-category"),

    # Products
    path("product/list/", ListProductAPIView.as_view(), name="list-products"),
    path("product/create/", CreateProductAPIView.as_view(), name="create-product"),
    path("product/<int:pk>/detail/", DetailProductAPIView.as_view(), name="product-detail"),
    path("product/<int:pk>/update/", UpdateProductAPIView.as_view(), name="update-product"),
    path("product/<int:pk>/delete/", DeleteProductAPIView.as_view(), name="delete-product"),
]
