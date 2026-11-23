from pathlib import Path
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.core.files.storage import FileSystemStorage

from config.models import SnakeCaseModel


def private_report_storage():
    return FileSystemStorage(location=settings.PRIVATE_MEDIA_ROOT)


def patient_report_upload_to(instance, filename):
    suffix = Path(filename).suffix.lower()
    return f"records/patient_{instance.patient_id}/{uuid4().hex}{suffix}"


class MedicalReport(SnakeCaseModel):
    class Status(models.TextChoices):
        UPLOADED = "uploaded", "Uploaded"
        PROCESSING = "processing", "AI processing"
        READY = "ready", "Explanation ready"
        FAILED = "failed", "Failed"

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="medical_reports",
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(
        upload_to=patient_report_upload_to,
        storage=private_report_storage,
    )
    treatment_need = models.CharField(max_length=120, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.UPLOADED,
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self) -> str:
        return f"{self.title} ({self.patient})"
