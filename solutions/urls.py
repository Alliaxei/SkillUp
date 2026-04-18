from django.urls import path

from .views import StudentResultsListView, TaskSubmissionView

app_name = "solutions"

urlpatterns = [
    path("task/<int:pk>/", TaskSubmissionView.as_view(), name="task_detail"),
    path("results/", StudentResultsListView.as_view(), name="student_results"),
]
