from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import (
    PatientLoginForm,
    PatientProfileForm,
    PatientRegistrationForm,
    ProviderLoginForm,
)
from .mixins import PatientRequiredMixin, signed_in_home
from .models import PatientProfile


class PatientRegisterView(CreateView):
    form_class = PatientRegistrationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("records:dashboard")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(signed_in_home(request.user))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class PatientLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = PatientLoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(signed_in_home(request.user))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("records:dashboard")


class ProviderLoginView(LoginView):
    template_name = "accounts/provider_login.html"
    authentication_form = ProviderLoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(signed_in_home(request.user))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        home = signed_in_home(self.request.user)
        return reverse(home or "marketplace:home")


class PatientLogoutView(LogoutView):
    next_page = reverse_lazy("marketplace:home")


class PatientProfileUpdateView(PatientRequiredMixin, UpdateView):
    model = PatientProfile
    form_class = PatientProfileForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("records:dashboard")

    def get_object(self, queryset=None):
        return self.request.user.patient_profile
