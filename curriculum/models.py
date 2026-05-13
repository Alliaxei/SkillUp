from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from core.models import BaseModel


class Module(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Название модуля")
    description = models.TextField(verbose_name="Описание модуля")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок отображения")

    class Meta:
        verbose_name = "Учебный модуль"
        verbose_name_plural = "Учебные модули"
        ordering = ["order"]

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
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Лекция"
        verbose_name_plural = "Лекции"
        ordering = ["order"]


class LectureImage(models.Model):
    lecture = models.ForeignKey(
        Lecture, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="lectures/%Y/%m/", verbose_name="Изображение")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Изображение лекции"
        verbose_name_plural = "Изображения лекций"
