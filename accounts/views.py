from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import PatientLoginForm, PatientRegistrationForm


class PatientRegisterView(CreateView):
    form_class = PatientRegistrationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("records:dashboard")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class PatientLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = PatientLoginForm
    redirect_authenticated_user = True


class PatientLogoutView(LogoutView):
    next_page = reverse_lazy("marketplace:home")
