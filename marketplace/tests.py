from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings
from django.urls import reverse

from providers.models import Doctor, Hospital, TreatmentPackage


class ProductionMarketplaceVisibilityTests(TestCase):
    @override_settings(DEBUG=False)
    def test_public_pages_exclude_sample_providers_and_their_packages(self):
        sample_hospital = Hospital.objects.create(
            name="Sample Hospital",
            slug="sample-hospital",
            city="Sample City",
            summary="Fictional listing",
            is_sample=True,
        )
        approved_hospital = Hospital.objects.create(
            name="Approved Hospital",
            slug="approved-hospital",
            city="Approved City",
            summary="Approved listing",
            is_sample=False,
        )
        Doctor.objects.create(
            name="Sample Doctor",
            slug="sample-doctor",
            hospital=approved_hospital,
            is_sample=True,
        )
        Doctor.objects.create(
            name="Unapproved Hospital Doctor",
            slug="unapproved-hospital-doctor",
            hospital=sample_hospital,
            is_sample=False,
        )
        approved_doctor = Doctor.objects.create(
            name="Approved Doctor",
            slug="approved-doctor",
            hospital=approved_hospital,
            is_sample=False,
        )
        TreatmentPackage.objects.create(
            name="Sample Package",
            slug="sample-package",
            hospital=sample_hospital,
        )
        TreatmentPackage.objects.create(
            name="Approved Package",
            slug="approved-package",
            hospital=approved_hospital,
        )

        home = self.client.get(reverse("marketplace:home"))
        hospital_list = self.client.get(reverse("marketplace:hospitals"))
        doctor_list = self.client.get(reverse("marketplace:doctors"))

        self.assertEqual(list(home.context["hospitals"]), [approved_hospital])
        self.assertEqual(list(home.context["doctors"]), [approved_doctor])
        self.assertEqual(
            list(home.context["packages"].values_list("name", flat=True)),
            ["Approved Package"],
        )
        self.assertEqual(list(hospital_list.context["hospitals"]), [approved_hospital])
        self.assertEqual(list(doctor_list.context["doctors"]), [approved_doctor])
        approved_detail = self.client.get(
            reverse("marketplace:hospital_detail", args=[approved_hospital.slug])
        )
        self.assertEqual(
            list(approved_detail.context["hospital"].doctors.all()),
            [approved_doctor],
        )
        self.assertEqual(
            list(
                approved_detail.context["hospital"]
                .packages.values_list("name", flat=True)
            ),
            ["Approved Package"],
        )
        self.assertEqual(
            self.client.get(
                reverse("marketplace:hospital_detail", args=[sample_hospital.slug])
            ).status_code,
            404,
        )
        self.assertEqual(
            self.client.get(
                reverse("marketplace:doctor_detail", args=["unapproved-hospital-doctor"])
            ).status_code,
            404,
        )
        self.assertEqual(
            self.client.get(
                reverse("marketplace:doctor_detail", args=[approved_doctor.slug])
            ).status_code,
            200,
        )

    @override_settings(DEBUG=True)
    def test_debug_mode_keeps_sample_listings_available(self):
        sample_hospital = Hospital.objects.create(
            name="Sample Hospital",
            slug="sample-hospital",
            city="Sample City",
            summary="Fictional listing",
            is_sample=True,
        )

        response = self.client.get(reverse("marketplace:hospitals"))

        self.assertEqual(list(response.context["hospitals"]), [sample_hospital])

    @override_settings(DEBUG=False)
    def test_sample_seed_command_is_blocked_when_debug_is_disabled(self):
        with self.assertRaisesMessage(
            CommandError,
            "Sample marketplace data can only be seeded when DEBUG is enabled.",
        ):
            call_command("seed_marketplace")

        self.assertFalse(Hospital.objects.exists())
