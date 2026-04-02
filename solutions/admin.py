from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html

from .models import Review, Submission


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 0
    can_delete = False
    verbose_name = "Результат проверки"


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("student", "task", "colored_status", "created_at", "get_score")
    list_filter = ("status", "task__module", "created_at")
    search_fields = ("student__last_name", "student__username", "task__title")
    readonly_fields = ("created_at", "updated_at")
    inlines = [ReviewInline]

    @admin.display(description="Статус")
    def colored_status(self, obj: Submission) -> str:
        colors = {
            Submission.Status.PENDING: "orange",
            Submission.Status.REVIEWING: "blue",
            Submission.Status.COMPLETED: "green",
            Submission.Status.REVISION: "red",
        }
        color = colors.get(obj.status, "black")
        display_text = obj.get_status_display()

        return format_html('<b style="color: {};">{}</b>', color, display_text)

    @admin.display(description="Оценка")
    def get_score(self, obj: Submission) -> str | int:
        if hasattr(obj, "review"):
            return obj.review.score
        return "—"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("submission", "teacher", "score", "created_at")
    list_filter = ("teacher", "score")
    autocomplete_fields = ("submission",)
    search_fields = ("submission__student__last_name", "comment")

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return (
            super()
            .get_queryset(request)
            .select_related("submission", "teacher", "submission__student")
        )
