from django.urls import path

from .views import (
    LectureCreateView,
    LectureDetailView,
    MaterialDetailView,
    ModuleCreateView,
    ModuleDetailView,
    ModuleListView,
    TaskCreateView,
    TaskListView,
)

app_name = "curriculum"

urlpatterns = [
    path("modules/", ModuleListView.as_view(), name="module_list"),
    path("modules/<int:pk>/", ModuleDetailView.as_view(), name="module_detail"),
    path("modules/create/", ModuleCreateView.as_view(), name="module_create"),
    path("materials/<int:pk>/", MaterialDetailView.as_view(), name="material_detail"),
    path("tasks/", TaskListView.as_view(), name="task_list"),
    path("tasks/create/", TaskCreateView.as_view(), name="task_create"),
    path("lectures/create/", LectureCreateView.as_view(), name="lecture_create"),
    path("lectures/<int:pk>/", LectureDetailView.as_view(), name="lecture_detail"),
]
