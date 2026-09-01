from django.urls import path

from .views import (
    PatientLoginView,
    PatientLogoutView,
    PatientProfileUpdateView,
    PatientRegisterView,
    ProviderLoginView,
)

app_name = "accounts"

urlpatterns = [
    path("register/", PatientRegisterView.as_view(), name="register"),
    path("login/", PatientLoginView.as_view(), name="login"),
    path("provider/login/", ProviderLoginView.as_view(), name="provider_login"),
    path("logout/", PatientLogoutView.as_view(), name="logout"),
    path("profile/", PatientProfileUpdateView.as_view(), name="profile"),
]
