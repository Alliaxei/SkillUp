import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, IntegerField, Value, When
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView, UpdateView

from curriculum.models import Task
from curriculum.views import TeacherRequiredMixin

from .forms import SubmissionForm
from .models import Review, Submission
from .selectors import get_student_submissions
from .services import SubmissionService

logger = logging.getLogger(__name__)


class TaskSubmissionView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "solutions/task_detail.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SubmissionForm()
        context["user_submission"] = self.object.submissions.filter(
            student=self.request.user
        ).first()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if request.user.role != "student":
            messages.error(
                request, "Только студенты могут отправлять работы на проверку."
            )
            return redirect("solutions:task_detail", pk=self.object.id)

        existing_submission = self.object.submissions.filter(
            student=request.user
        ).exists()

        if existing_submission:
            logger.warning(
                f"Пользователь {request.user} пытался повторно отправить работу для задания {self.object.id}"
            )
            messages.error(
                request,
                "Вы уже отправили работу на проверку. Повторная отправка невозможна.",
            )
            return redirect("solutions:task_detail", pk=self.object.id)

        form = SubmissionForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                SubmissionService.create_submission(
                    student=request.user,
                    task_id=self.object.id,
                    uploaded_file=request.FILES.get("file"),
                )
                messages.success(request, "Работа успешно отправлена на проверку.")
            except Exception as e:
                logger.error(f"Ошибка в SubmissionService: {str(e)}")
                messages.error(request, f"Ошибка: {str(e)}")
        else:
            for error in form.errors.values():
                messages.error(request, error.as_text())

        return redirect("solutions:task_detail", pk=self.object.id)


class StudentResultsListView(LoginRequiredMixin, ListView):
    template_name = "solutions/student_results.html"
    context_object_name = "submissions"

    def get_queryset(self):
        return get_student_submissions(self.request.user)


class TeacherSubmissionListView(TeacherRequiredMixin, ListView):
    model = Submission
    template_name = "solutions/teacher_submissions.html"
    context_object_name = "submissions"

    def get_queryset(self):
        queryset = Submission.objects.select_related("student", "task", "task__module")

        if not self.request.user.is_superuser:
            queryset = queryset.filter(student__teacher=self.request.user)

        return queryset.annotate(
            status_priority=Case(
                When(status=Submission.Status.PENDING, then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            )
        ).order_by("status_priority", "-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        visible_submissions = self.get_queryset()
        context["pending_count"] = visible_submissions.filter(
            status=Submission.Status.PENDING
        ).count()

        return context


class ReviewCreateView(TeacherRequiredMixin, UpdateView):
    model = Review
    fields = ["score", "comment"]
    template_name = "solutions/review_form.html"

    def get_object(self, queryset=None):
        submission_id = self.kwargs.get("submission_id")
        submission = get_object_or_404(Submission, id=submission_id)
        review, created = Review.objects.get_or_create(
            submission=submission, defaults={"teacher": self.request.user, "score": 0}
        )
        return review

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["submission"] = self.object.submission
        return context

    def form_valid(self, form):
        review = form.save(commit=False)
        review.teacher = self.request.user
        review.save()

        submission = review.submission
        submission.status = (
            Submission.Status.COMPLETED
            if review.score > 0
            else Submission.Status.REVISION
        )
        submission.save()

        messages.success(
            self.request,
            f"Результат проверки для {submission.student.get_full_name()} сохранен.",
        )
        return redirect("solutions:teacher_submissions")
