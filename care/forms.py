from django import forms
from django.utils import timezone
from django.utils.timezone import get_current_timezone, is_naive, make_aware
from django.utils.text import slugify

from providers.models import Doctor, Hospital, TreatmentPackage

from .models import Appointment, AvailabilitySlot, ProcedureHistory, SuggestedTest


class ProcedureHistoryForm(forms.ModelForm):
    class Meta:
        model = ProcedureHistory
        fields = ("procedure_name", "year", "facility_name", "notes")


class SlotForm(forms.ModelForm):
    class Meta:
        model = AvailabilitySlot
        fields = ("starts_at", "ends_at", "is_blocked", "notes")
        widgets = {
            "starts_at": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M", attrs={"type": "datetime-local"}
            ),
            "ends_at": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M", attrs={"type": "datetime-local"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ("starts_at", "ends_at"):
            self.fields[name].input_formats = ["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S"]

    def clean(self):
        cleaned = super().clean()
        starts = cleaned.get("starts_at")
        ends = cleaned.get("ends_at")
        tz = get_current_timezone()
        if starts and is_naive(starts):
            starts = make_aware(starts, tz)
            cleaned["starts_at"] = starts
        if ends and is_naive(ends):
            ends = make_aware(ends, tz)
            cleaned["ends_at"] = ends
        if starts and ends and ends <= starts:
            raise forms.ValidationError("End time must be after the start time.")
        if starts and starts <= timezone.now():
            raise forms.ValidationError("Slots must be in the future.")
        return cleaned


class AppointmentRequestForm(forms.Form):
    slot = forms.ModelChoiceField(queryset=AvailabilitySlot.objects.none(), required=True)
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 3}))

    def __init__(self, *args, doctor=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.doctor = doctor
        qs = AvailabilitySlot.objects.filter(doctor=doctor, is_blocked=False, starts_at__gt=timezone.now())
        bookable_ids = [slot.pk for slot in qs if slot.is_bookable()]
        self.fields["slot"].queryset = AvailabilitySlot.objects.filter(pk__in=bookable_ids)
        self.fields["slot"].label = "Open slot"


class AppointmentNoteForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ("notes",)


class SuggestedTestForm(forms.ModelForm):
    class Meta:
        model = SuggestedTest
        fields = ("patient", "name", "reason")

    def __init__(self, *args, doctor=None, **kwargs):
        super().__init__(*args, **kwargs)
        from django.contrib.auth.models import User

        patient_ids = (
            Appointment.objects.filter(doctor=doctor)
            .values_list("patient_id", flat=True)
            .distinct()
        )
        self.fields["patient"].queryset = User.objects.filter(pk__in=patient_ids)


class HospitalPageForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = (
            "name",
            "city",
            "accreditation",
            "summary",
            "image_url",
            "typical_stay",
            "tags",
            "features",
        )


class HospitalDoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = (
            "name",
            "title",
            "specialty",
            "city",
            "years_experience",
            "bio",
            "languages",
            "initials",
            "is_active",
        )


class HospitalPackageForm(forms.ModelForm):
    class Meta:
        model = TreatmentPackage
        fields = (
            "name",
            "specialty",
            "typical_stay",
            "approx_cost_from",
            "approx_cost_to",
            "approx_cost_currency",
            "includes",
            "excludes",
            "is_active",
        )

    def save(self, commit=True):
        package = super().save(commit=False)
        if not package.slug:
            base = slugify(package.name)[:160] or "package"
            slug = base
            suffix = 1
            while TreatmentPackage.objects.filter(slug=slug).exclude(pk=package.pk).exists():
                slug = f"{base}-{suffix}"
                suffix += 1
            package.slug = slug
        if commit:
            package.save()
        return package
