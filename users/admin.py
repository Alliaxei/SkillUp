from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "last_name",
        "first_name",
        "middle_name",
        "is_staff",
    )
    search_fields = ("username", "last_name", "email")
    list_filter = ("is_staff", "is_superuser", "groups")

    fieldsets = UserAdmin.fieldsets + (("Дополнительно", {"fields": ("middle_name",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Дополнительно", {"fields": ("middle_name",)}),
    )
