from django import forms
from django.conf import settings

from .models import MedicalReport
from .validators import validate_medical_report_file


class MedicalReportFileValidationMixin:
    def clean_file(self):
        uploaded_file = self.cleaned_data["file"]
        validate_medical_report_file(uploaded_file)
        return uploaded_file


class MedicalReportUploadForm(MedicalReportFileValidationMixin, forms.ModelForm):
    class Meta:
        model = MedicalReport
        fields = ("title", "treatment_need", "description", "file")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "file": forms.ClearableFileInput(
                attrs={"accept": ".pdf,.jpg,.jpeg,.png,.docx"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["file"].help_text = (
            "Accepted formats: PDF, JPEG, PNG, DOCX. "
            f"Maximum size: {settings.MAX_REPORT_UPLOAD_SIZE_MB} MB."
        )
