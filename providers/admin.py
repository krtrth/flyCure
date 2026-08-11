from django.contrib import admin

from .models import Doctor, Hospital, Specialty, TreatmentPackage


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ("name", "short_code", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "short_code")


class DoctorInline(admin.TabularInline):
    model = Doctor
    extra = 0
    fields = ("name", "specialty", "years_experience", "is_active")


class PackageInline(admin.TabularInline):
    model = TreatmentPackage
    extra = 0
    fields = ("name", "specialty", "typical_stay", "is_active")


@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "accreditation", "is_sample", "is_active")
    list_filter = ("city", "is_sample", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "city", "accreditation")
    filter_horizontal = ("specialties",)
    inlines = [DoctorInline, PackageInline]


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("name", "specialty", "hospital", "city", "years_experience", "is_active")
    list_filter = ("city", "specialty", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "city", "languages")


@admin.register(TreatmentPackage)
class TreatmentPackageAdmin(admin.ModelAdmin):
    list_display = ("name", "hospital", "specialty", "typical_stay", "is_active")
    list_filter = ("specialty", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "hospital__name")
