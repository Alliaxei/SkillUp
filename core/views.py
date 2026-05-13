from django.views.generic import TemplateView

from solutions.models import Submission
from users.models import User


class IndexView(TemplateView):
    def get_template_names(self) -> list[str]:
        if not self.request.user.is_authenticated:
            return ["pages/index.html"]

        if self.request.user.role == User.Role.TEACHER or self.request.user.is_staff:
            return ["pages/teacher_dashboard.html"]
        return ["pages/dashboard.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated and (user.role == User.Role.TEACHER or user.is_staff):
            context["total_students"] = User.objects.filter(
                teacher=user, role=User.Role.STUDENT
            ).count()

            context["pending_count"] = Submission.objects.filter(
                student__teacher=user, status=Submission.Status.PENDING
            ).count()

        return context


class AboutView(TemplateView):
    template_name = "pages/about.html"
