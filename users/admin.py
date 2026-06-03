from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission

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
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "Персональные данные",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "middle_name",
                    "email",
                    "role",
                    "group",
                )
            },
        ),
        ("Права доступа", {"fields": ("is_active", "is_staff")}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("middle_name", "role", "group")}),
    )


if admin.site.is_registered(Group):
    admin.site.unregister(Group)

if admin.site.is_registered(Permission):
    admin.site.unregister(Permission)
