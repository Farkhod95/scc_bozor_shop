from django.urls import path, include

urlpatterns = [
    path('v1/', include('apps.uploads.v1.urls')),
]