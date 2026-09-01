from django.conf import settings
from django.db import models
from django.utils import timezone

from config.models import SnakeCaseModel
from providers.models import Doctor


class ProcedureHistory(SnakeCaseModel):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="procedure_history",
    )
    procedure_name = models.CharField(max_length=200)
    year = models.PositiveIntegerField(null=True, blank=True)
    facility_name = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-year", "-created_at"]

    def __str__(self) -> str:
        return f"{self.procedure_name} ({self.patient})"


class SuggestedTest(SnakeCaseModel):
    class Status(models.TextChoices):
        SUGGESTED = "suggested", "Suggested"
        COMPLETED = "completed", "Completed"

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="suggested_tests",
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="suggested_tests",
    )
    name = models.CharField(max_length=200)
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUGGESTED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} for {self.patient}"


class AvailabilitySlot(SnakeCaseModel):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="slots")
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    is_blocked = models.BooleanField(default=False)
    notes = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["starts_at"]

    def __str__(self) -> str:
        return f"{self.doctor} {self.starts_at:%Y-%m-%d %H:%M}"

    def is_bookable(self) -> bool:
        if self.is_blocked or self.starts_at <= timezone.now():
            return False
        return not self.appointments.filter(
            status__in=[Appointment.Status.REQUESTED, Appointment.Status.CONFIRMED]
        ).exists()


class Appointment(SnakeCaseModel):
    class Status(models.TextChoices):
        REQUESTED = "requested", "Requested"
        CONFIRMED = "confirmed", "Confirmed"
        DECLINED = "declined", "Declined"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    class Source(models.TextChoices):
        SITE = "site", "On-site slot request"
        WHATSAPP = "whatsapp", "WhatsApp"

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appointments",
    )
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")
    slot = models.ForeignKey(
        AvailabilitySlot,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="appointments",
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.REQUESTED)
    source = models.CharField(max_length=20, choices=Source.choices, default=Source.SITE)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.patient} × {self.doctor} ({self.status})"
