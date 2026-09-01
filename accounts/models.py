from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django.db import models

from config.models import SnakeCaseModel


class PatientProfile(SnakeCaseModel):
    class Gender(models.TextChoices):
        FEMALE = "female", "Female"
        MALE = "male", "Male"
        OTHER = "other", "Other"
        UNSPECIFIED = "unspecified", "Prefer not to say"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_profile",
    )
    country = models.CharField(max_length=100, blank=True)
    phone_whatsapp = models.CharField(max_length=32, blank=True)
    mobile = models.CharField(max_length=32, blank=True)
    preferred_language = models.CharField(max_length=50, blank=True, default="English")
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=Gender.choices, blank=True)
    height_cm = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    bmi = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.user.get_full_name() or self.user.username} ({self.country or 'n/a'})"

    @property
    def age(self):
        if not self.date_of_birth:
            return None
        today = date.today()
        years = today.year - self.date_of_birth.year
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            years -= 1
        return years

    def recalculate_bmi(self):
        if self.height_cm and self.weight_kg and self.height_cm > 0:
            height_m = Decimal(self.height_cm) / Decimal("100")
            self.bmi = (Decimal(self.weight_kg) / (height_m * height_m)).quantize(
                Decimal("0.1"), rounding=ROUND_HALF_UP
            )
        else:
            self.bmi = None

    def save(self, *args, **kwargs):
        if not self.mobile and self.phone_whatsapp:
            self.mobile = self.phone_whatsapp
        self.recalculate_bmi()
        super().save(*args, **kwargs)
