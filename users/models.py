from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import BaseModel
from curriculum.models import StudentGroup


class User(AbstractUser, BaseModel):
    class Role(models.TextChoices):
        STUDENT = "student", "Студент"
        TEACHER = "teacher", "Преподаватель"

    middle_name = models.CharField(max_length=150, blank=True, verbose_name="Отчество")
    role = models.CharField(
        max_length=10, choices=Role.choices, default=Role.STUDENT, verbose_name="Роль"
    )
    group = models.ForeignKey(
        StudentGroup,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
        verbose_name="Учебная группа",
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["last_name", "first_name"]

    def __str__(self) -> str:
        full_name = f"{self.last_name} {self.first_name} {self.middle_name}".strip()
        return full_name if full_name else self.username

    @property
    def header_display_name(self):
        if self.is_superuser:
            return "Администратор"

        role_map = {"teacher": "Преподаватель", "student": "Студент"}
        display_role = role_map.get(self.role, "Пользователь")

        return f"{self.first_name} {self.last_name} ({display_role})"
