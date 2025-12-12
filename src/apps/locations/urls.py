from django.urls import path, include

urlpatterns = [
    path('v1/', include('apps.locations.v1.urls')),
]
