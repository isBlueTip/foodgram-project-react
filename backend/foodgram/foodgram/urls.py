from django.conf import settings  # TODO dev settings
from django.conf.urls.static import static  # TODO dev settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)  # TODO dev settings
