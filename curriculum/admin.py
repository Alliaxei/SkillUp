from django.contrib import admin

from .models import Material, Module, Task


class MaterialInline(admin.TabularInline):
    model = Material
    extra = 1
    fields = ("title", "file", "text_content")


class TaskInline(admin.StackedInline):
    model = Task
    extra = 1
    fields = ("title", "deadline", "max_score")


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    list_display_links = ("title",)
    inlines = [MaterialInline, TaskInline]


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("title", "module", "created_at")
    list_filter = ("module",)
    search_fields = ("title",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "module", "deadline", "max_score")
    list_filter = ("module", "deadline")
    date_hierarchy = "deadline"
