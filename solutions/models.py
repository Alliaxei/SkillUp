from django.conf import settings
from django.db import models

from core.models import BaseModel
from curriculum.models import Task


class Submission(BaseModel):
    class Status(models.TextChoices):
        PENDING = "pending", "Ожидает проверки"
        REVIEWING = "reviewing", "На проверке"
        COMPLETED = "completed", "Проверено"
        REVISION = "revision", "Нужна доработка"

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="submissions",
        verbose_name="Задание",
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="submissions",
        verbose_name="Студент",
    )
    file = models.FileField(
        upload_to="submissions/%Y/%m/", verbose_name="Файл с решением"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Статус проверки",
    )

    class Meta:
        verbose_name = "Отправленная работа"
        verbose_name_plural = "Отправленные работы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Работа: {self.student.last_name} - {self.task.title}"


class Review(BaseModel):
    submission = models.OneToOneField(
        Submission,
        on_delete=models.CASCADE,
        related_name="review",
        verbose_name="Работа",
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="reviews_given",
        verbose_name="Проверяющий преподаватель",
    )
    comment = models.TextField(verbose_name="Комментарий преподавателя")
    score = models.PositiveIntegerField(verbose_name="Полученный балл")

    class Meta:
        verbose_name = "Рецензия"
        verbose_name_plural = "Рецензии"

    def __str__(self):
        return f"Рецензия на работу {self.submission.id}"
