from django.urls import path

from .views import (
    DoctorDetailView,
    DoctorListView,
    HomeView,
    HospitalDetailView,
    HospitalListView,
)

app_name = "marketplace"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("hospitals/", HospitalListView.as_view(), name="hospitals"),
    path("hospitals/<slug:slug>/", HospitalDetailView.as_view(), name="hospital_detail"),
    path("doctors/", DoctorListView.as_view(), name="doctors"),
    path("doctors/<slug:slug>/", DoctorDetailView.as_view(), name="doctor_detail"),
]
