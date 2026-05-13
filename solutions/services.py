import logging

from django.core.exceptions import ValidationError
from django.utils import timezone

from curriculum.models import Task
from users.models import User

from .models import Submission

logger = logging.getLogger(__name__)


class SubmissionService:
    @staticmethod
    def create_submission(student, task_id, uploaded_file) -> Submission:
        task = Task.objects.get(id=task_id)
        current_date = timezone.now().date()

        if task.deadline:
            if task.deadline < current_date:
                raise ValidationError("Срок сдачи задания истек.")

        if not uploaded_file:
            raise ValidationError("Файл решения не найден.")

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
