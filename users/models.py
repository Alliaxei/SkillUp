from django.contrib.auth.models import AbstractUser
from django.db import models

from core.models import BaseModel


class User(AbstractUser, BaseModel):
    middle_name = models.CharField(max_length=150, blank=True, verbose_name="Отчество")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        full_name = f"{self.last_name} {self.first_name} {self.middle_name}".strip()
        return full_name if full_name else self.username
