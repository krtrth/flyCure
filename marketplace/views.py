from django.db.models import Q
from django.views.generic import DetailView, ListView, TemplateView

from providers.models import Doctor, Hospital, Specialty, TreatmentPackage


class HomeView(TemplateView):
    template_name = "marketplace/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "").strip()
        specialty = self.request.GET.get("specialty", "all")
        city = self.request.GET.get("city", "all")

        specialties = Specialty.objects.filter(is_active=True)
        hospitals = Hospital.objects.filter(is_active=True).prefetch_related("specialties")
        doctors = Doctor.objects.filter(is_active=True).select_related("specialty", "hospital")
        packages = TreatmentPackage.objects.filter(is_active=True).select_related(
            "hospital", "specialty"
        )

        if query:
            hospitals = hospitals.filter(
                Q(name__icontains=query)
                | Q(city__icontains=query)
                | Q(summary__icontains=query)
                | Q(specialties__name__icontains=query)
            ).distinct()
            doctors = doctors.filter(
                Q(name__icontains=query)
                | Q(bio__icontains=query)
                | Q(city__icontains=query)
                | Q(specialty__name__icontains=query)
            )
            packages = packages.filter(
                Q(name__icontains=query) | Q(hospital__name__icontains=query)
            )
            specialties_filtered = specialties.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        else:
            specialties_filtered = specialties

        if specialty != "all":
            hospitals = hospitals.filter(specialties__short_code=specialty).distinct()
            doctors = doctors.filter(specialty__short_code=specialty)
            packages = packages.filter(specialty__short_code=specialty)
            specialties_filtered = specialties_filtered.filter(short_code=specialty)

        if city != "all":
            hospitals = hospitals.filter(city=city)
            doctors = doctors.filter(Q(city=city) | Q(hospital__city=city))

        cities = (
            Hospital.objects.filter(is_active=True)
            .values_list("city", flat=True)
            .distinct()
            .order_by("city")
        )

        context.update(
            {
                "specialties": specialties_filtered,
                "all_specialties": specialties,
                "hospitals": hospitals,
                "doctors": doctors,
                "packages": packages,
                "cities": cities,
                "filters": {
                    "q": query,
                    "specialty": specialty,
                    "city": city,
                },
            }
        )
        return context


class HospitalListView(ListView):
    model = Hospital
    template_name = "marketplace/hospitals.html"
    context_object_name = "hospitals"

    def get_queryset(self):
        qs = Hospital.objects.filter(is_active=True).prefetch_related("specialties")
        q = self.request.GET.get("q", "").strip()
        city = self.request.GET.get("city", "all")
        specialty = self.request.GET.get("specialty", "all")
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(summary__icontains=q) | Q(city__icontains=q))
        if city != "all":
            qs = qs.filter(city=city)
        if specialty != "all":
            qs = qs.filter(specialties__short_code=specialty).distinct()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_specialties"] = Specialty.objects.filter(is_active=True)
        context["cities"] = (
            Hospital.objects.filter(is_active=True)
            .values_list("city", flat=True)
            .distinct()
            .order_by("city")
        )
        context["filters"] = {
            "q": self.request.GET.get("q", ""),
            "specialty": self.request.GET.get("specialty", "all"),
            "city": self.request.GET.get("city", "all"),
        }
        return context


class HospitalDetailView(DetailView):
    model = Hospital
    template_name = "marketplace/hospital_detail.html"
    context_object_name = "hospital"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Hospital.objects.filter(is_active=True).prefetch_related(
            "specialties", "doctors", "packages"
        )


class DoctorListView(ListView):
    model = Doctor
    template_name = "marketplace/doctors.html"
    context_object_name = "doctors"

    def get_queryset(self):
        qs = Doctor.objects.filter(is_active=True).select_related("specialty", "hospital")
        q = self.request.GET.get("q", "").strip()
        city = self.request.GET.get("city", "all")
        specialty = self.request.GET.get("specialty", "all")
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(bio__icontains=q) | Q(city__icontains=q))
        if city != "all":
            qs = qs.filter(Q(city=city) | Q(hospital__city=city))
        if specialty != "all":
            qs = qs.filter(specialty__short_code=specialty)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_specialties"] = Specialty.objects.filter(is_active=True)
        context["cities"] = (
            Doctor.objects.filter(is_active=True)
            .values_list("city", flat=True)
            .distinct()
            .order_by("city")
        )
        context["filters"] = {
            "q": self.request.GET.get("q", ""),
            "specialty": self.request.GET.get("specialty", "all"),
            "city": self.request.GET.get("city", "all"),
        }
        return context


class DoctorDetailView(DetailView):
    model = Doctor
    template_name = "marketplace/doctor_detail.html"
    context_object_name = "doctor"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Doctor.objects.filter(is_active=True).select_related("specialty", "hospital")
