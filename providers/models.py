from django.conf import settings
from django.db import models

from config.models import SnakeCaseModel


class Specialty(SnakeCaseModel):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    short_code = models.CharField(max_length=40, blank=True, help_text="Filter key, e.g. cardiac")
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=8, blank=True, default="+")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "specialties"

    def __str__(self) -> str:
        return self.name


class Hospital(SnakeCaseModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    city = models.CharField(max_length=100)
    accreditation = models.CharField(max_length=120, blank=True)
    summary = models.TextField()
    image_url = models.URLField(blank=True)
    typical_stay = models.CharField(max_length=80, blank=True)
    features = models.TextField(
        blank=True,
        help_text="Facilities shown on the public hospital page, one per line or a short paragraph.",
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="linked_hospital",
    )
    tags = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated tags shown on cards",
    )
    specialties = models.ManyToManyField(Specialty, related_name="hospitals", blank=True)
    is_sample = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.city})"

    @property
    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]

    @property
    def primary_specialty_code(self):
        specialty = self.specialties.first()
        return specialty.short_code if specialty else ""


class Doctor(SnakeCaseModel):
    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    title = models.CharField(max_length=120, blank=True)
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="doctors",
    )
    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="doctors",
    )
    city = models.CharField(max_length=100, blank=True)
    years_experience = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True)
    languages = models.CharField(max_length=200, blank=True)
    initials = models.CharField(max_length=4, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="linked_doctor",
    )
    is_sample = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    @property
    def specialty_code(self):
        return self.specialty.short_code if self.specialty else ""


class TreatmentPackage(SnakeCaseModel):
    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    hospital = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        related_name="packages",
    )
    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="packages",
    )
    typical_stay = models.CharField(max_length=80, blank=True)
    approx_cost_from = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    approx_cost_to = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )
    approx_cost_currency = models.CharField(max_length=8, blank=True, default="USD")
    includes = models.TextField(blank=True)
    excludes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    @property
    def specialty_code(self):
        return self.specialty.short_code if self.specialty else ""

    @property
    def approx_cost_label(self):
        if self.approx_cost_from is None and self.approx_cost_to is None:
            return ""
        currency = self.approx_cost_currency or "USD"
        if self.approx_cost_from is not None and self.approx_cost_to is not None:
            return f"{currency} {self.approx_cost_from:,.0f}–{self.approx_cost_to:,.0f}"
        amount = self.approx_cost_from if self.approx_cost_from is not None else self.approx_cost_to
        return f"from {currency} {amount:,.0f}"
