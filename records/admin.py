from django.contrib import admin

from .models import MedicalReport


@admin.register(MedicalReport)
class MedicalReportAdmin(admin.ModelAdmin):
    list_display = ("title", "patient", "treatment_need", "status", "uploaded_at")
    list_filter = ("status", "treatment_need")
    search_fields = ("title", "patient__username", "patient__email")
    readonly_fields = ("uploaded_at", "updated_at")
