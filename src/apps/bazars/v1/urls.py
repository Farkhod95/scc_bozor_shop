from django.urls import path
from apps.bazars.views import *

app_name = "catalog"

urlpatterns = [
    # Bazars
    path("bazar/list/", ListBazarAPIView.as_view(), name="list-bazars"),
    path("bazar/create/", CreateBazarAPIView.as_view(), name="create-bazar"),
]