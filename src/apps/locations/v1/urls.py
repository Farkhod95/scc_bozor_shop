from django.urls import path
from apps.locations.views import *

app_name = "locations"

urlpatterns = [
    # Regions
    path("region/list/", ListRegionAPIView.as_view(), name="list-regions"),
    path("region/create/", CreateRegionAPIView.as_view(), name="create-region"),
    path("region/<int:pk>/detail/", DetailRegionAPIView.as_view(), name="detail-region"),
    path("region/<int:pk>/update/", UpdateRegionAPIView.as_view(), name="update-region"),
    path("region/<int:pk>/delete/", DeleteRegionAPIView.as_view(), name="delete-region"),

    # Cities
    path("city/list/", ListCityAPIView.as_view(), name="list-cities"),
    path("city/create/", CreateCityAPIView.as_view(), name="create-city"),
    path("city/<int:pk>/detail/", DetailCityAPIView.as_view(), name="detail-city"),
    path("city/<int:pk>/update/", UpdateCityAPIView.as_view(), name="update-city"),
    path("city/<int:pk>/delete/", DeleteCityAPIView.as_view(), name="delete-city"),
]