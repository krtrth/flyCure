from django import forms
from django.contrib import admin

from .forms import MedicalReportFileValidationMixin
from .models import MedicalReport


class MedicalReportAdminForm(MedicalReportFileValidationMixin, forms.ModelForm):
    class Meta:
        model = MedicalReport
        fields = "__all__"


@admin.register(MedicalReport)
class MedicalReportAdmin(admin.ModelAdmin):
    form = MedicalReportAdminForm
    list_display = ("title", "patient", "treatment_need", "status", "uploaded_at")
    list_filter = ("status", "treatment_need")
    search_fields = ("title", "patient__username", "patient__email")
    readonly_fields = ("uploaded_at", "updated_at")
