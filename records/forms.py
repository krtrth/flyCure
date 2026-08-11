from django import forms

from .models import MedicalReport


class MedicalReportUploadForm(forms.ModelForm):
    class Meta:
        model = MedicalReport
        fields = ("title", "treatment_need", "description", "file")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }
