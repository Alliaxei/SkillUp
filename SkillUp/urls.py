from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("curriculum/", include("curriculum.urls")),
    path("solutions/", include("solutions.urls")),
    path("", include("core.urls")),
]
