from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "middle_name",
        "role",
        "group",
        "is_staff",
    )
    search_fields = ("username", "last_name", "email")

    list_filter = ("role", "group", "is_staff", "is_superuser", "is_active")
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("middle_name", "role", "group")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("middle_name", "role", "group")}),
    )
