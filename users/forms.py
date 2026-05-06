from idlelib.debugobj_r import remote_object_tree_item
from typing import Any

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control btn-rounded", "placeholder": "Логин"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control btn-rounded", "placeholder": "Пароль"}
        )
    )


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    middle_name = forms.CharField(label="Отчество", required=False)
    email = forms.EmailField(label="Email")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "last_name", "first_name", "middle_name", "email")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "form-control btn-rounded px-3 py-2",
                    "placeholder": field.label,
                }
            )
