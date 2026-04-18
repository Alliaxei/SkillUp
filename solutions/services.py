from django.core.exceptions import ValidationError
from django.utils import timezone

from curriculum.models import Task
from users.models import User

from .models import Submission


class SubmissionService:
    @staticmethod
    def create_submission(student: User, task_id: int, uploaded_file) -> Submission:
        task = Task.objects.get(id=task_id)

        if task.deadline < timezone.now():
            raise ValidationError("Срок сдачи задания истек.")

        submission, created = Submission.objects.update_or_create(
            student=student,
            task=task,
            defaults={
                "file": uploaded_file,
                "status": Submission.Status.PENDING,
                "updated_at": timezone.now(),
            },
        )
        return submission
