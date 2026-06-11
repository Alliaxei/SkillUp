import logging
from datetime import date

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, QuerySet
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from solutions.models import Submission
from users.models import User

from .forms import LectureForm, ModuleForm, TaskForm
from .models import Lecture, LectureImage, Material, Module, StudentGroup, Task


class ModuleListView(LoginRequiredMixin, ListView):
    model = Module
    template_name = "curriculum/module_list.html"
    context_object_name = "modules"

    def get(self, request, *args, **kwargs):
        if request.user.role == "student" and not request.user.group:
            return render(request, "curriculum/no_group.html")
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return Module.objects.annotate(
            lectures_count=Count("lectures"), tasks_count=Count("tasks")
        )


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
            context["today"] = date.today().strftime("%Y-%m-%d")
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

    def get_success_url(self):
        return reverse("curriculum:module_detail", kwargs={"pk": self.object.module.id})


class LectureDetailView(LoginRequiredMixin, DetailView):
    model = Lecture
    template_name = "curriculum/lecture_detail.html"
    context_object_name = "lecture"


class TeacherGroupsListView(LoginRequiredMixin, ListView):
    model = StudentGroup
    template_name = "curriculum/teacher_groups.html"
    context_object_name = "groups"

    def get_queryset(self):
        user = self.request.user
        logger.info("--- Отладка списков групп ---")
        logger.info(
            f"Пользователь: {user.username}, ID: {user.id}, Роль: {user.role}, Админ: {user.is_superuser}"
        )

        total_in_db = StudentGroup.objects.count()
        logger.info(f"Всего групп в базе данных (без фильтров): {total_in_db}")

        if user.is_superuser:
            queryset = StudentGroup.objects.all()
            logger.info(
                f"Запрос от администратора. Возвращаем все группы. Найдено: {queryset.count()}"
            )
        else:
            queryset = StudentGroup.objects.filter(teacher=user)
            logger.info(
                f"Запрос от преподавателя. Фильтр по teacher_id={user.id}. Найдено: {queryset.count()}"
            )

        return queryset


class GroupCreateView(LoginRequiredMixin, CreateView):
    model = StudentGroup
    fields = ["title"]
    success_url = reverse_lazy("curriculum:teacher_groups_list")

    def form_valid(self, form):
        user = self.request.user
        form.instance.teacher = user

        logger.info("--- Отладка создания группы ---")
        logger.info(
            f"Пытаемся создать группу с названием: {form.cleaned_data['title']}"
        )
        logger.info(f"Создатель: {user.username} (ID: {user.id}, Роль: {user.role})")

        response = super().form_valid(form)

        logger.info(
            f"Группа успешно сохранена в БД. ID новой группы: {self.object.id}, Владелец (teacher_id): {self.object.teacher_id}"
        )

        messages.success(
            self.request, f"Группа «{form.cleaned_data['title']}» успешно создана."
        )
        return response

    def form_invalid(self, form):
        if "title" in form.errors:
            entered_title = self.request.POST.get("title", "неизвестное")
            messages.error(
                self.request, f'Группа с названием "{entered_title}" уже существует.'
            )
        else:
            messages.error(
                self.request, "Ошибка при создании группы. Проверьте данные."
            )

        logger.error(f"Ошибка валидации формы создания группы: {form.errors}")

        return redirect("curriculum:teacher_groups_list")


class GroupDetailView(LoginRequiredMixin, DetailView):
    model = StudentGroup
    template_name = "curriculum/group_detail.html"
    context_object_name = "group"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = self.object.students.all()

        context["available_students"] = User.objects.filter(
            role=User.Role.STUDENT, group__isnull=True
        )
        return context


class AddStudentToGroupView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        group = get_object_or_404(StudentGroup, pk=pk)
        student_id = request.POST.get("student_id")

        if student_id:
            student = get_object_or_404(
                User, id=student_id, role=User.Role.STUDENT, group__isnull=True
            )
            student.group = group
            student.save()
            messages.success(
                request,
                f"Обучающийся {student.get_full_name()} успешно добавлен в группу.",
            )
        else:
            messages.error(request, "Обучающийся не был выбран.")

        return redirect("curriculum:group_detail", pk=group.pk)


class RemoveStudentFromGroupView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        group = get_object_or_404(StudentGroup, pk=pk)
        student_id = request.POST.get("student_id")

        if student_id:
            student = get_object_or_404(
                User, id=student_id, role=User.Role.STUDENT, group=group
            )
            student.group = None
            student.save()
            messages.success(
                request,
                f"Обучающийся {student.get_full_name()} успешно исключен из группы.",
            )
        else:
            messages.error(request, "Обучающийся не был указан.")

        return redirect("curriculum:group_detail", pk=group.pk)


class TaskUpdateView(TeacherRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "curriculum/task_form.html"

    def get_success_url(self):
        messages.success(
            self.request, f"Задание «{self.object.title}» успешно обновлено."
        )
        return reverse_lazy("solutions:task_detail", kwargs={"pk": self.object.pk})


class LectureUpdateView(TeacherRequiredMixin, UpdateView):
    model = Lecture
    form_class = LectureForm
    template_name = "curriculum/lecture_form.html"

    def get_success_url(self):
        messages.success(
            self.request, f"Лекция «{self.object.title}» успешно обновлена."
        )
        return reverse_lazy("curriculum:lecture_detail", kwargs={"pk": self.object.pk})


class ModuleUpdateView(TeacherRequiredMixin, UpdateView):
    model = Module
    form_class = ModuleForm
    template_name = "curriculum/module_form.html"

    def get_success_url(self):
        messages.success(
            self.request, f"Модуль «{self.object.title}» успешно обновлен."
        )
        return reverse_lazy("curriculum:module_detail", kwargs={"pk": self.object.pk})
