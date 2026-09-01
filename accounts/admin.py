from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import PatientProfile


class PatientProfileInline(admin.StackedInline):
    model = PatientProfile
    can_delete = False
    extra = 0


class UserAdmin(BaseUserAdmin):
    inlines = [PatientProfileInline]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "country", "mobile", "gender", "bmi", "created_at")
    search_fields = ("user__username", "user__email", "country", "mobile", "phone_whatsapp")
