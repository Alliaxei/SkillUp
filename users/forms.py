import re
from typing import Any

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.validators import RegexValidator

from users.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(
            attrs={"class": "form-control btn-rounded", "placeholder": "Логин"}
        ),
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control btn-rounded", "placeholder": "Пароль"}
        ),
    )


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label="Имя",
    )
    last_name = forms.CharField(
        label="Фамилия",
    )
    middle_name = forms.CharField(label="Отчество", required=False)
    email = forms.EmailField(label="Email")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "last_name", "first_name", "middle_name", "email")
        labels = {
            "username": "Логин",
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "form-control btn-rounded px-3 py-2",
                    "placeholder": field.label,
                }
            )

    def _validate_name(self, value: str) -> str:
        if not re.fullmatch(r"[А-Яа-яЁё-]+", value):
            raise forms.ValidationError("Допускаются только буквы кириллицы и дефис.")

        if value.startswith("-") or value.endswith("-"):
            raise forms.ValidationError("Дефис не может находиться в начале или конце.")

        if "--" in value:
            raise forms.ValidationError(
                "Недопустимо использование двух дефисов подряд."
            )

        return value

    def clean_first_name(self) -> str:
        return self._validate_name(self.cleaned_data["first_name"])

    def clean_last_name(self) -> str:
        return self._validate_name(self.cleaned_data["last_name"])

    def clean_middle_name(self) -> str:
        value = self.cleaned_data["middle_name"]

        if not value:
            return value

        return self._validate_name(value)
