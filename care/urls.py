from django.urls import path

from .views import (
    AppointmentCancelView,
    AppointmentRequestView,
    DoctorAppointmentActionView,
    DoctorDashboardView,
    DoctorSlotCreateView,
    DoctorSlotDeleteView,
    DoctorTestCreateView,
    HospitalDashboardView,
    HospitalDoctorUpdateView,
    HospitalPackageCreateView,
    HospitalPackageUpdateView,
    HospitalPageUpdateView,
    ProcedureHistoryCreateView,
    ProcedureHistoryDeleteView,
)

app_name = "care"

urlpatterns = [
    path("history/add/", ProcedureHistoryCreateView.as_view(), name="history_add"),
    path("history/<int:pk>/delete/", ProcedureHistoryDeleteView.as_view(), name="history_delete"),
    path(
        "appointments/request/<slug:slug>/",
        AppointmentRequestView.as_view(),
        name="appointment_request",
    ),
    path(
        "appointments/<int:pk>/cancel/",
        AppointmentCancelView.as_view(),
        name="appointment_cancel",
    ),
    path("doctor/", DoctorDashboardView.as_view(), name="doctor_dashboard"),
    path("doctor/slots/add/", DoctorSlotCreateView.as_view(), name="doctor_slot_add"),
    path("doctor/slots/<int:pk>/delete/", DoctorSlotDeleteView.as_view(), name="doctor_slot_delete"),
    path(
        "doctor/appointments/<int:pk>/<str:action>/",
        DoctorAppointmentActionView.as_view(),
        name="doctor_appointment_action",
    ),
    path("doctor/tests/add/", DoctorTestCreateView.as_view(), name="doctor_test_add"),
    path("hospital/", HospitalDashboardView.as_view(), name="hospital_dashboard"),
    path("hospital/page/", HospitalPageUpdateView.as_view(), name="hospital_page"),
    path(
        "hospital/doctors/<int:pk>/",
        HospitalDoctorUpdateView.as_view(),
        name="hospital_doctor_edit",
    ),
    path("hospital/packages/add/", HospitalPackageCreateView.as_view(), name="hospital_package_add"),
    path(
        "hospital/packages/<int:pk>/",
        HospitalPackageUpdateView.as_view(),
        name="hospital_package_edit",
    ),
]
