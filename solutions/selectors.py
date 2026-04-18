from django.db.models import QuerySet

from .models import Submission


def get_student_submissions(user) -> QuerySet:
    return (
        Submission.objects.filter(student=user)
        .select_related("task", "task__module", "review")
        .order_by("-created_at")
    )
