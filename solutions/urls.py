from django.urls import path

from .views import (
    ReviewCreateView,
    ReviewDetailView,
    StudentResultsListView,
    TaskSubmissionView,
    TeacherSubmissionListView,
)

app_name = "solutions"

urlpatterns = [
    path("task/<int:pk>/", TaskSubmissionView.as_view(), name="task_detail"),
    path("results/", StudentResultsListView.as_view(), name="student_results"),
    path(
        "teacher/submissions/",
        TeacherSubmissionListView.as_view(),
        name="teacher_submissions",
    ),
    path(
        "teacher/review/<int:submission_id>/",
        ReviewCreateView.as_view(),
        name="review_create",
    ),
    path(
        "teacher/submissions/<int:submission_id>/result/",
        ReviewDetailView.as_view(),
        name="review_detail",
    ),
]
