from django.urls import path

from .views import AboutView, IndexView

app_name = "core"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("about/", AboutView.as_view(), name="about"),
]
