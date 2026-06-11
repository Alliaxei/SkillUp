from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Административная панель"
admin.site.site_title = "Администрирование"
admin.site.index_title = "Управление системой"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("curriculum/", include("curriculum.urls")),
    path("solutions/", include("solutions.urls")),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("", include("core.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
