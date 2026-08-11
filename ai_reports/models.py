from django.conf import settings
from django.db import models

from records.models import MedicalReport


class ReportExplanation(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETE = "complete", "Complete"
        FAILED = "failed", "Failed"

    report = models.OneToOneField(
        MedicalReport,
        on_delete=models.CASCADE,
        related_name="explanation",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    summary = models.TextField(blank=True)
    key_findings = models.TextField(blank=True)
    patient_friendly_notes = models.TextField(blank=True)
    disclaimer = models.TextField(
        blank=True,
        default=(
            "This explanation is informational only and does not replace a doctor's "
            "review. Final treatment decisions require clinical assessment."
        ),
    )
    model_name = models.CharField(max_length=80, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        return f"Explanation for {self.report_id} ({self.status})"
