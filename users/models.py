from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import BaseModel


class User(AbstractUser, BaseModel):
    class Role(models.TextChoices):
        STUDENT = "student", "Студент"
        TEACHER = "teacher", "Преподаватель"

    middle_name = models.CharField(max_length=150, blank=True, verbose_name="Отчество")
    role = models.CharField(
        max_length=10, choices=Role.choices, default=Role.STUDENT, verbose_name="Роль"
    )
    teacher = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"role": "teacher"},
        related_name="students",
        verbose_name="Закрепленный преподаватель",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["last_name", "first_name"]

    def __str__(self) -> str:
        full_name = f"{self.last_name} {self.first_name} {self.middle_name}".strip()
        return full_name if full_name else self.username
