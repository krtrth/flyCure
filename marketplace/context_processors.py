from django.conf import settings
from django.urls import reverse

from accounts.mixins import is_doctor, is_hospital, is_patient, signed_in_home


def site_settings(request):
    user = getattr(request, "user", None)
    portal_label = "Patient login"
    portal_url = reverse("accounts:login")
    if user and user.is_authenticated:
        if is_doctor(user):
            portal_label = "Doctor desk"
        elif is_hospital(user):
            portal_label = "Hospital desk"
        elif is_patient(user):
            portal_label = "My records"
        elif user.is_staff or user.is_superuser:
            portal_label = "Admin"
        else:
            portal_label = user.get_username()
        portal_url = reverse(signed_in_home(user))
    return {
        "WHATSAPP_NUMBER": settings.WHATSAPP_NUMBER,
        "SITE_NAME": "FlyCure",
        "portal_label": portal_label,
        "portal_url": portal_url,
        "is_patient_user": is_patient(user) if user else False,
        "is_doctor_user": is_doctor(user) if user else False,
        "is_hospital_user": is_hospital(user) if user else False,
    }
