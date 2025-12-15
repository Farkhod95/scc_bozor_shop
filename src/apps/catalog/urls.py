from django.urls import path, include


urlpatterns = [
    path('v1/', include('apps.catalog.v1.urls')),
]
