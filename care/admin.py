from django.contrib import admin

from .models import Appointment, AvailabilitySlot, ProcedureHistory, SuggestedTest


@admin.register(ProcedureHistory)
class ProcedureHistoryAdmin(admin.ModelAdmin):
    list_display = ("patient", "procedure_name", "year", "facility_name")
    search_fields = ("procedure_name", "patient__username")


@admin.register(SuggestedTest)
class SuggestedTestAdmin(admin.ModelAdmin):
    list_display = ("patient", "name", "doctor", "status", "created_at")
    list_filter = ("status",)


@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(admin.ModelAdmin):
    list_display = ("doctor", "starts_at", "ends_at", "is_blocked")
    list_filter = ("is_blocked", "doctor")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "status", "source", "slot", "created_at")
    list_filter = ("status", "source")
    search_fields = ("patient__username", "doctor__name")
