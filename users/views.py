from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserLoginForm, UserRegisterForm


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "registration/login.html"


class UserLogoutView(LogoutView):
    next_page = "core:index"


class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("users:login")
