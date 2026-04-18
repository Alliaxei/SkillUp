from django.views.generic import TemplateView


class IndexView(TemplateView):
    def get_template_names(self) -> list[str]:
        if self.request.user.is_authenticated:
            return ["pages/dashboard.html"]
        return ["pages/index.html"]


class AboutView(TemplateView):
    template_name = "pages/about.html"
