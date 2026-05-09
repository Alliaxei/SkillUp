from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, QuerySet
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from users.models import User

from .forms import ModuleForm, TaskForm
from .models import Material, Module, Task
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

    def get_queryset(self):
        return Task.objects.select_related("module").order_by("deadline")


class ModuleDetailView(LoginRequiredMixin, DetailView):
    model = Module
    template_name = "curriculum/module_detail.html"
    context_object_name = "module"

    def get_object(self, queryset: QuerySet | None = None) -> Module:
        return get_module_with_content(self.kwargs.get("pk"))


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
