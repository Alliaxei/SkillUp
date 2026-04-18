from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, QuerySet
from django.shortcuts import render
from django.views.generic import DetailView, ListView

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
