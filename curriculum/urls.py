from django.urls import path

from .views import (
    AddStudentToGroupView,
    GroupCreateView,
    GroupDetailView,
    LectureCreateView,
    LectureDetailView,
    LectureUpdateView,
    MaterialDetailView,
    ModuleCreateView,
    ModuleDetailView,
    ModuleListView,
    ModuleUpdateView,
    RemoveStudentFromGroupView,
    TaskCreateView,
    TaskListView,
    TaskUpdateView,
    TeacherGroupsListView,
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
    path(
        "teacher/groups/", TeacherGroupsListView.as_view(), name="teacher_groups_list"
    ),
    path("teacher/groups/create/", GroupCreateView.as_view(), name="group_create"),
    path("teacher/groups/<int:pk>/", GroupDetailView.as_view(), name="group_detail"),
    path(
        "teacher/groups/<int:pk>/add-student/",
        AddStudentToGroupView.as_view(),
        name="add_student_to_group",
    ),
    path(
        "teacher/groups/<int:pk>/remove-student/",
        RemoveStudentFromGroupView.as_view(),
        name="remove_student_from_group",
    ),
    path("tasks/<int:pk>/edit/", TaskUpdateView.as_view(), name="task_edit"),
    path("lectures/<int:pk>/edit/", LectureUpdateView.as_view(), name="lecture_edit"),
    path("modules/<int:pk>/edit/", ModuleUpdateView.as_view(), name="module_edit"),
]
