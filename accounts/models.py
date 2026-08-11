from django.conf import settings
from django.db import models


class PatientProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_profile",
    )
    country = models.CharField(max_length=100, blank=True)
    phone_whatsapp = models.CharField(max_length=32, blank=True)
    preferred_language = models.CharField(max_length=50, blank=True, default="English")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.user.get_full_name() or self.user.username} ({self.country or 'n/a'})"
