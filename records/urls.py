from django.urls import path

from .views import (
    PatientDashboardView,
    ReportDetailView,
    ReportUploadView,
    RequestExplanationView,
)

app_name = "records"

urlpatterns = [
    path("", PatientDashboardView.as_view(), name="dashboard"),
    path("upload/", ReportUploadView.as_view(), name="upload"),
    path("<int:pk>/", ReportDetailView.as_view(), name="report_detail"),
    path("<int:pk>/explain/", RequestExplanationView.as_view(), name="request_explanation"),
]
