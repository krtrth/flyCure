from django.urls import path

from .views import PatientLoginView, PatientLogoutView, PatientRegisterView

app_name = "accounts"

urlpatterns = [
    path("register/", PatientRegisterView.as_view(), name="register"),
    path("login/", PatientLoginView.as_view(), name="login"),
    path("logout/", PatientLogoutView.as_view(), name="logout"),
]
