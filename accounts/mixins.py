from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.shortcuts import redirect


def _related_or_none(user, attr):
    if not getattr(user, "is_authenticated", False):
        return None
    try:
        return getattr(user, attr)
    except (ObjectDoesNotExist, AttributeError):
        return None


def is_patient(user):
    return _related_or_none(user, "patient_profile") is not None


def is_doctor(user):
    return _related_or_none(user, "linked_doctor") is not None


def is_hospital(user):
    return _related_or_none(user, "linked_hospital") is not None


def provider_home_url(user):
    if is_doctor(user) and is_hospital(user):
        return None
    if is_doctor(user):
        return "care:doctor_dashboard"
    if is_hospital(user):
        return "care:hospital_dashboard"
    return None


def signed_in_home(user):
    """Named URL for whoever is currently logged in."""
    if not getattr(user, "is_authenticated", False):
        return None
    provider = provider_home_url(user)
    if provider:
        return provider
    if is_patient(user):
        return "records:dashboard"
    if getattr(user, "is_staff", False) or getattr(user, "is_superuser", False):
        return "admin:index"
    return "marketplace:home"


class PatientRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if is_doctor(request.user) or is_hospital(request.user):
            home = provider_home_url(request.user)
            if home:
                return redirect(home)
            raise PermissionDenied("This area is for patients.")
        if not is_patient(request.user):
            home = signed_in_home(request.user)
            if home:
                return redirect(home)
            raise PermissionDenied("Create a patient profile to continue.")
        return super().dispatch(request, *args, **kwargs)


class DoctorRequiredMixin(LoginRequiredMixin):
    login_url = "accounts:provider_login"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not is_doctor(request.user) or is_hospital(request.user):
            raise PermissionDenied("Doctor access only.")
        return super().dispatch(request, *args, **kwargs)


class HospitalRequiredMixin(LoginRequiredMixin):
    login_url = "accounts:provider_login"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not is_hospital(request.user) or is_doctor(request.user):
            raise PermissionDenied("Hospital access only.")
        return super().dispatch(request, *args, **kwargs)
