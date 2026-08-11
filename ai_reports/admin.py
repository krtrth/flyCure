from django.contrib import admin

from .models import ReportExplanation


@admin.register(ReportExplanation)
class ReportExplanationAdmin(admin.ModelAdmin):
    list_display = ("report", "status", "model_name", "updated_at")
    list_filter = ("status", "model_name")
    search_fields = ("report__title", "summary")
    readonly_fields = ("created_at", "updated_at")
