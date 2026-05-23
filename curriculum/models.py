from django.conf import settings
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from core.models import BaseModel


class StudentGroup(BaseModel):
    title = models.CharField(
        max_length=100, unique=True, verbose_name="Название группы"
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"role": "teacher"},
        related_name="student_groups",
        verbose_name="Преподаватель/Куратор",
    )

    class Meta:
        verbose_name = "Учебная группа"
        verbose_name_plural = "Учебные группы"
        ordering = ["title"]

    def __str__(self):
        return self.title


class Module(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Название модуля")
    description = models.TextField(verbose_name="Описание модуля")

    class Meta:
        verbose_name = "Учебный модуль"
        verbose_name_plural = "Учебные модули"
        ordering = ["title"]

    def __str__(self):
        return self.title


class Material(BaseModel):
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="materials",
        verbose_name="Модуль",
    )
    title = models.CharField(max_length=255, verbose_name="Заголовок материала")
    file = models.FileField(
        upload_to="materials/%Y/%m/",
        verbose_name="Файл материала",
        blank=True,
        null=True,
    )
    text_content = models.TextField(blank=True, verbose_name="Текстовое содержание")

    class Meta:
        verbose_name = "Учебный материал"
        verbose_name_plural = "Учебные материалы"

    def __str__(self):
        return self.title


class Task(BaseModel):
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="tasks", verbose_name="Модуль"
    )
    title = models.CharField(max_length=255, verbose_name="Название задания")
    description = models.TextField(verbose_name="Техническое задание")
    deadline = models.DateField(verbose_name="Крайний срок сдачи")
    max_score = models.PositiveIntegerField(
        default=100, verbose_name="Максимальный балл"
    )

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"
        ordering = ["deadline"]

    def __str__(self):
        return self.title


class Lecture(BaseModel):
    module = models.ForeignKey(
        Module, on_delete=models.CASCADE, related_name="lectures", verbose_name="Модуль"
    )
    title = models.CharField(max_length=255, verbose_name="Название лекции")
    content = CKEditor5Field(verbose_name="Содержание лекции", config_name="default")

    class Meta:
        verbose_name = "Лекция"
        verbose_name_plural = "Лекции"
        ordering = ["title"]


class LectureImage(models.Model):
    lecture = models.ForeignKey(
        Lecture, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="lectures/%Y/%m/", verbose_name="Изображение")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Изображение лекции"
        verbose_name_plural = "Изображения лекций"
