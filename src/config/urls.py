from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django_prometheus import exports
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # OpenAPI schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Swagger UI
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    # ReDoc UI
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    path('admin/', admin.site.urls),

    path("api/accounts/", include("apps.accounts.urls")),
    path("api/catalog/", include("apps.catalog.urls")),
    path("api/bazars/", include("apps.bazars.urls")),
    path("api/uploads/", include("apps.uploads.urls")),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
