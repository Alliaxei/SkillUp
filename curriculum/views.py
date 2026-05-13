import logging

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from solutions.models import Submission
from users.models import User

from .forms import LectureForm, ModuleForm, TaskForm
from .models import Lecture, LectureImage, Material, Module, Task
from .selectors import get_module_with_content


class ModuleListView(LoginRequiredMixin, ListView):
    model = Module
    template_name = "curriculum/module_list.html"
    context_object_name = "modules"

    def get_queryset(self):
        return Module.objects.annotate(
            materials_count=Count("materials"), tasks_count=Count("tasks")
        ).order_by("order")


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "curriculum/task_list.html"
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            submitted_task_ids = Submission.objects.filter(
                student=self.request.user
            ).values_list("task_id", flat=True)

            context["submitted_task_ids"] = set(submitted_task_ids)
        return context


class ModuleDetailView(LoginRequiredMixin, DetailView):
    model = Module
    template_name = "curriculum/module_detail.html"
    context_object_name = "module"

    def get_queryset(self) -> QuerySet:
        return Module.objects.prefetch_related("lectures", "tasks")


class MaterialDetailView(LoginRequiredMixin, DetailView):
    model = Material
    template_name = "curriculum/material_detail.html"
    context_object_name = "material"


class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        return self.request.user.is_authenticated and (
            self.request.user.role == User.Role.TEACHER or self.request.user.is_staff
        )


class ModuleCreateView(TeacherRequiredMixin, CreateView):
    model = Module
    form_class = ModuleForm
    template_name = "curriculum/module_form.html"
    success_url = reverse_lazy("curriculum:module_list")

    def form_valid(self, form):
        last_module = Module.objects.order_by("-order").first()
        form.instance.order = (last_module.order + 1) if last_module else 1
        return super().form_valid(form)


class TaskCreateView(TeacherRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "curriculum/task_form.html"
    success_url = reverse_lazy("curriculum:task_list")


logger = logging.getLogger(__name__)


class LectureCreateView(TeacherRequiredMixin, CreateView):
    model = Lecture
    form_class = LectureForm
    template_name = "curriculum/lecture_form.html"

    def form_valid(self, form):
        logger.info(f"Форма лекции валидна. Пользователь: {self.request.user}")
        lecture = form.save()

        images = self.request.FILES.getlist("images")
        logger.info(f"Загружено дополнительных изображений: {len(images)}")

        for img in images:
            LectureImage.objects.create(lecture=lecture, image=img)

        logger.info(f"Лекция '{lecture.title}' успешно создана (ID: {lecture.id})")
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.warning(f"Ошибка валидации формы лекции: {form.errors.as_json()}")
        return super().form_invalid(form)


class LectureDetailView(LoginRequiredMixin, DetailView):
    model = Lecture
    template_name = "curriculum/lecture_detail.html"
    context_object_name = "lecture"
