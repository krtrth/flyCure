from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, FormView, TemplateView, UpdateView, View

from accounts.mixins import DoctorRequiredMixin, HospitalRequiredMixin, PatientRequiredMixin
from providers.models import Doctor

from .forms import (
    AppointmentRequestForm,
    HospitalDoctorForm,
    HospitalPackageForm,
    HospitalPageForm,
    ProcedureHistoryForm,
    SlotForm,
    SuggestedTestForm,
)
from .models import Appointment, AvailabilitySlot, ProcedureHistory, SuggestedTest


class ProcedureHistoryCreateView(PatientRequiredMixin, CreateView):
    model = ProcedureHistory
    form_class = ProcedureHistoryForm
    template_name = "care/history_form.html"
    success_url = reverse_lazy("records:dashboard")

    def form_valid(self, form):
        form.instance.patient = self.request.user
        messages.success(self.request, "Procedure added to your history.")
        return super().form_valid(form)


class ProcedureHistoryDeleteView(PatientRequiredMixin, View):
    def post(self, request, pk):
        item = get_object_or_404(ProcedureHistory, pk=pk, patient=request.user)
        item.delete()
        messages.success(request, "Procedure removed.")
        return redirect("records:dashboard")


class AppointmentRequestView(PatientRequiredMixin, FormView):
    template_name = "care/appointment_request.html"
    form_class = AppointmentRequestForm

    def dispatch(self, request, *args, **kwargs):
        self.doctor = get_object_or_404(Doctor, slug=kwargs["slug"], is_active=True)
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["doctor"] = self.doctor
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctor"] = self.doctor
        return context

    def form_valid(self, form):
        slot = form.cleaned_data["slot"]
        if slot.doctor_id != self.doctor.pk or not slot.is_bookable():
            messages.error(self.request, "That slot is no longer available.")
            return self.form_invalid(form)
        Appointment.objects.create(
            patient=self.request.user,
            doctor=self.doctor,
            slot=slot,
            notes=form.cleaned_data.get("notes", ""),
            status=Appointment.Status.REQUESTED,
            source=Appointment.Source.SITE,
        )
        messages.success(
            self.request,
            "Request sent. A doctor or coordinator will confirm the slot.",
        )
        return redirect("records:dashboard")


class AppointmentCancelView(PatientRequiredMixin, View):
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk, patient=request.user)
        if appointment.status in {Appointment.Status.REQUESTED, Appointment.Status.CONFIRMED}:
            appointment.status = Appointment.Status.CANCELLED
            appointment.save(update_fields=["status", "updated_at"])
            messages.success(request, "Appointment cancelled.")
        return redirect("records:dashboard")


class DoctorDashboardView(DoctorRequiredMixin, TemplateView):
    template_name = "care/doctor_dashboard.html"
    login_url = reverse_lazy("accounts:provider_login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.request.user.linked_doctor
        now = timezone.now()
        appointments = Appointment.objects.filter(doctor=doctor).select_related("patient", "slot")
        context.update(
            {
                "doctor": doctor,
                "requests": appointments.filter(status=Appointment.Status.REQUESTED),
                "upcoming": appointments.filter(
                    status=Appointment.Status.CONFIRMED, slot__starts_at__gte=now
                ),
                "past_patients": User.objects.filter(
                    appointments__doctor=doctor,
                    appointments__status__in=[
                        Appointment.Status.CONFIRMED,
                        Appointment.Status.COMPLETED,
                    ],
                ).distinct(),
                "slots": AvailabilitySlot.objects.filter(doctor=doctor, starts_at__gte=now)[:40],
            }
        )
        return context


class DoctorSlotCreateView(DoctorRequiredMixin, CreateView):
    model = AvailabilitySlot
    form_class = SlotForm
    template_name = "care/slot_form.html"
    success_url = reverse_lazy("care:doctor_dashboard")
    login_url = reverse_lazy("accounts:provider_login")

    def form_valid(self, form):
        form.instance.doctor = self.request.user.linked_doctor
        messages.success(self.request, "Slot added.")
        return super().form_valid(form)


class DoctorSlotDeleteView(DoctorRequiredMixin, View):
    login_url = reverse_lazy("accounts:provider_login")

    def post(self, request, pk):
        slot = get_object_or_404(AvailabilitySlot, pk=pk, doctor=request.user.linked_doctor)
        if slot.appointments.filter(
            status__in=[Appointment.Status.REQUESTED, Appointment.Status.CONFIRMED]
        ).exists():
            messages.error(request, "Cannot delete a slot that has an active request.")
        else:
            slot.delete()
            messages.success(request, "Slot removed.")
        return redirect("care:doctor_dashboard")


class DoctorAppointmentActionView(DoctorRequiredMixin, View):
    login_url = reverse_lazy("accounts:provider_login")

    def post(self, request, pk, action):
        appointment = get_object_or_404(
            Appointment, pk=pk, doctor=request.user.linked_doctor
        )
        mapping = {
            "confirm": Appointment.Status.CONFIRMED,
            "decline": Appointment.Status.DECLINED,
            "complete": Appointment.Status.COMPLETED,
        }
        if action in mapping:
            appointment.status = mapping[action]
            appointment.save(update_fields=["status", "updated_at"])
            messages.success(request, f"Appointment marked {mapping[action]}.")
        return redirect("care:doctor_dashboard")


class DoctorTestCreateView(DoctorRequiredMixin, CreateView):
    form_class = SuggestedTestForm
    template_name = "care/test_form.html"
    success_url = reverse_lazy("care:doctor_dashboard")
    login_url = reverse_lazy("accounts:provider_login")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["doctor"] = self.request.user.linked_doctor
        return kwargs

    def form_valid(self, form):
        form.instance.doctor = self.request.user.linked_doctor
        messages.success(self.request, "Test suggested for the patient.")
        return super().form_valid(form)


class HospitalDashboardView(HospitalRequiredMixin, TemplateView):
    template_name = "care/hospital_dashboard.html"
    login_url = reverse_lazy("accounts:provider_login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hospital = self.request.user.linked_hospital
        context.update(
            {
                "hospital": hospital,
                "doctors": hospital.doctors.all(),
                "packages": hospital.packages.all(),
                "appointments": Appointment.objects.filter(doctor__hospital=hospital)
                .select_related("patient", "doctor", "slot")[:50],
            }
        )
        return context


class HospitalPageUpdateView(HospitalRequiredMixin, UpdateView):
    form_class = HospitalPageForm
    template_name = "care/hospital_page_form.html"
    success_url = reverse_lazy("care:hospital_dashboard")
    login_url = reverse_lazy("accounts:provider_login")

    def get_object(self, queryset=None):
        return self.request.user.linked_hospital


class HospitalDoctorUpdateView(HospitalRequiredMixin, UpdateView):
    form_class = HospitalDoctorForm
    template_name = "care/hospital_doctor_form.html"
    success_url = reverse_lazy("care:hospital_dashboard")
    login_url = reverse_lazy("accounts:provider_login")

    def get_queryset(self):
        return self.request.user.linked_hospital.doctors.all()


class HospitalPackageCreateView(HospitalRequiredMixin, CreateView):
    form_class = HospitalPackageForm
    template_name = "care/hospital_package_form.html"
    success_url = reverse_lazy("care:hospital_dashboard")
    login_url = reverse_lazy("accounts:provider_login")

    def form_valid(self, form):
        form.instance.hospital = self.request.user.linked_hospital
        messages.success(self.request, "Package saved.")
        return super().form_valid(form)


class HospitalPackageUpdateView(HospitalRequiredMixin, UpdateView):
    form_class = HospitalPackageForm
    template_name = "care/hospital_package_form.html"
    success_url = reverse_lazy("care:hospital_dashboard")
    login_url = reverse_lazy("accounts:provider_login")

    def get_queryset(self):
        return self.request.user.linked_hospital.packages.all()
