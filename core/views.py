from django.views.generic import TemplateView

from users.models import User


class IndexView(TemplateView):
    def get_template_names(self) -> list[str]:
        if not self.request.user.is_authenticated:
            return ["pages/index.html"]

        if self.request.user.role == User.Role.TEACHER or self.request.user.is_staff:
            return ["pages/teacher_dashboard.html"]
        return ["pages/dashboard.html"]


class AboutView(TemplateView):
    template_name = "pages/about.html"
