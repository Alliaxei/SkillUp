from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView

from curriculum.models import Task

from .forms import SubmissionForm
from .selectors import get_student_submissions
from .services import SubmissionService


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
        form = SubmissionForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                SubmissionService.create_submission(
                    student=request.user,
                    task_id=self.object.id,
                    uploaded_file=request.FILES["file"],
                )
                messages.success(request, "Работа успешно отправлена.")
            except Exception as e:
                messages.error(request, str(e))

        return redirect("solutions:task_detail", pk=self.object.id)


class StudentResultsListView(LoginRequiredMixin, ListView):
    template_name = "solutions/student_results.html"
    context_object_name = "submissions"

    def get_queryset(self):
        return get_student_submissions(self.request.user)
