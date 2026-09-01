from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, View

from accounts.mixins import PatientRequiredMixin
from ai_reports.services import queue_report_explanation
from care.models import Appointment, ProcedureHistory, SuggestedTest

from .forms import MedicalReportUploadForm
from .models import MedicalReport


class PatientDashboardView(PatientRequiredMixin, ListView):
    model = MedicalReport
    template_name = "records/dashboard.html"
    context_object_name = "reports"

    def get_queryset(self):
        return MedicalReport.objects.filter(patient=self.request.user).select_related(
            "explanation"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["profile"] = user.patient_profile
        context["appointments"] = Appointment.objects.filter(patient=user).select_related(
            "doctor", "slot"
        )
        context["suggested_tests"] = SuggestedTest.objects.filter(patient=user).select_related(
            "doctor"
        )
        context["history_items"] = ProcedureHistory.objects.filter(patient=user)
        return context


class ReportUploadView(PatientRequiredMixin, CreateView):
    model = MedicalReport
    form_class = MedicalReportUploadForm
    template_name = "records/upload.html"
    success_url = reverse_lazy("records:dashboard")

    def form_valid(self, form):
        form.instance.patient = self.request.user
        response = super().form_valid(form)
        queue_report_explanation(self.object)
        return response


class ReportDetailView(PatientRequiredMixin, DetailView):
    model = MedicalReport
    template_name = "records/report_detail.html"
    context_object_name = "report"

    def get_queryset(self):
        return MedicalReport.objects.filter(patient=self.request.user).select_related(
            "explanation"
        )


class RequestExplanationView(PatientRequiredMixin, View):
    def post(self, request, pk):
        report = get_object_or_404(MedicalReport, pk=pk, patient=request.user)
        queue_report_explanation(report, force=True)
        return redirect("records:report_detail", pk=report.pk)
