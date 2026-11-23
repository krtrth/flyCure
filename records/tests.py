from io import BytesIO
from unittest.mock import patch
from zipfile import ZipFile

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from accounts.models import PatientProfile
from records.admin import MedicalReportAdminForm
from records.forms import MedicalReportUploadForm
from records.models import MedicalReport
from records.scanning import scan_medical_report_file


class MedicalReportUploadValidationTests(TestCase):
    def make_form(self, uploaded_file):
        return MedicalReportUploadForm(
            data={"title": "Sample report", "treatment_need": "", "description": ""},
            files={"file": uploaded_file},
        )

    @patch("records.validators.scan_medical_report_file")
    def test_accepts_supported_formats_with_matching_signatures(self, scan_file):
        docx_content = BytesIO()
        with ZipFile(docx_content, "w") as archive:
            archive.writestr("[Content_Types].xml", "<Types/>")
            archive.writestr("word/document.xml", "<document/>")

        supported_files = (
            ("report.pdf", b"%PDF-1.7\n", "application/pdf"),
            ("report.jpg", b"\xff\xd8\xff\xdb", "image/jpeg"),
            ("report.png", b"\x89PNG\r\n\x1a\n", "image/png"),
            (
                "report.docx",
                docx_content.getvalue(),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ),
        )
        for filename, content, content_type in supported_files:
            with self.subTest(filename=filename):
                form = self.make_form(
                    SimpleUploadedFile(filename, content, content_type=content_type)
                )
                self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(scan_file.call_count, len(supported_files))

    def test_rejects_unsupported_extension(self):
        form = self.make_form(
            SimpleUploadedFile("report.exe", b"%PDF-", content_type="application/pdf")
        )

        self.assertFalse(form.is_valid())
        self.assertIn("Upload a PDF, JPEG, PNG, or DOCX file.", form.errors["file"])

    def test_rejects_mime_or_signature_mismatches(self):
        mismatched_mime = self.make_form(
            SimpleUploadedFile("report.pdf", b"%PDF-", content_type="text/plain")
        )
        mismatched_signature = self.make_form(
            SimpleUploadedFile("report.pdf", b"not a PDF", content_type="application/pdf")
        )

        self.assertFalse(mismatched_mime.is_valid())
        self.assertFalse(mismatched_signature.is_valid())

    def test_rejects_docx_without_required_package_parts(self):
        invalid_docx = BytesIO()
        with ZipFile(invalid_docx, "w") as archive:
            archive.writestr("not-a-document.txt", "invalid package")
        form = self.make_form(
            SimpleUploadedFile(
                "report.docx",
                invalid_docx.getvalue(),
                content_type=(
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                ),
            )
        )

        self.assertFalse(form.is_valid())
        self.assertIn("The uploaded file is not a valid DOCX document.", form.errors["file"])

    def test_admin_form_rejects_mismatched_signatures(self):
        user = get_user_model().objects.create_user(username="admin-form-patient")
        form = MedicalReportAdminForm(
            data={
                "patient": user.pk,
                "title": "Sample report",
                "treatment_need": "",
                "description": "",
                "status": MedicalReport.Status.UPLOADED,
            },
            files={
                "file": SimpleUploadedFile(
                    "report.pdf",
                    b"not a PDF",
                    content_type="application/pdf",
                )
            },
        )

        self.assertFalse(form.is_valid())
        self.assertIn("The uploaded file is not a valid PDF.", form.errors["file"])

    @override_settings(REPORT_UPLOADS_ENABLED=True)
    def test_upload_route_rejects_invalid_file_before_saving(self):
        user = get_user_model().objects.create_user(username="upload-form-patient")
        PatientProfile.objects.create(user=user)
        self.client.force_login(user)

        response = self.client.post(
            reverse("records:upload"),
            {
                "title": "Sample report",
                "treatment_need": "",
                "description": "",
                "file": SimpleUploadedFile(
                    "report.pdf",
                    b"not a PDF",
                    content_type="application/pdf",
                ),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(response.context["form"], "file", "The uploaded file is not a valid PDF.")
        self.assertFalse(MedicalReport.objects.exists())

    @patch(
        "records.validators.scan_medical_report_file",
        side_effect=ValidationError(
            "The uploaded file was flagged by malware scanning and was not saved."
        ),
    )
    @override_settings(REPORT_UPLOADS_ENABLED=True)
    def test_upload_route_does_not_save_a_flagged_file(self, scan_file):
        user = get_user_model().objects.create_user(username="flagged-upload-patient")
        PatientProfile.objects.create(user=user)
        self.client.force_login(user)

        response = self.client.post(
            reverse("records:upload"),
            {
                "title": "Sample report",
                "treatment_need": "",
                "description": "",
                "file": SimpleUploadedFile(
                    "report.pdf",
                    b"%PDF-1.7\n",
                    content_type="application/pdf",
                ),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormError(
            response.context["form"],
            "file",
            "The uploaded file was flagged by malware scanning and was not saved.",
        )
        self.assertFalse(MedicalReport.objects.exists())
        scan_file.assert_called_once()

    def test_uploads_are_disabled_and_upload_entry_points_are_hidden(self):
        user = get_user_model().objects.create_user(username="disabled-upload-patient")
        PatientProfile.objects.create(user=user)
        self.assertEqual(self.client.get(reverse("records:upload")).status_code, 302)
        self.client.force_login(user)

        page = self.client.get(reverse("records:upload"))
        self.assertEqual(page.status_code, 200)
        self.assertContains(page, "Report uploads are temporarily unavailable")
        self.assertNotContains(page, 'enctype="multipart/form-data"')

        response = self.client.post(
            reverse("records:upload"),
            {
                "title": "Should not save",
                "file": SimpleUploadedFile(
                    "report.pdf",
                    b"%PDF-1.7\n",
                    content_type="application/pdf",
                ),
            },
        )
        self.assertEqual(response.status_code, 405)
        self.assertFalse(MedicalReport.objects.exists())

        dashboard = self.client.get(reverse("records:dashboard"))
        self.assertNotContains(dashboard, reverse("records:upload"))
        self.assertContains(dashboard, "Report uploads are temporarily unavailable")

    @override_settings(MAX_REPORT_UPLOAD_SIZE_MB=1)
    def test_rejects_files_over_the_configured_size_limit(self):
        form = self.make_form(
            SimpleUploadedFile(
                "report.pdf",
                b"%PDF-" + b"x" * (1024 * 1024),
                content_type="application/pdf",
            )
        )

        self.assertFalse(form.is_valid())
        self.assertIn("The file must be no larger than 1 MB.", form.errors["file"])


class ClamAVScanningTests(TestCase):
    @patch("records.scanning._clamd_instream", return_value="stream: OK")
    def test_accepts_a_clean_scan_result(self, scan_stream):
        uploaded_file = SimpleUploadedFile("report.pdf", b"%PDF-1.7\n")

        scan_medical_report_file(uploaded_file)

        scan_stream.assert_called_once_with(uploaded_file)
        self.assertEqual(uploaded_file.tell(), 0)

    @patch(
        "records.scanning._clamd_instream",
        return_value="stream: Eicar-Test-Signature FOUND",
    )
    def test_rejects_a_flagged_file(self, scan_stream):
        uploaded_file = SimpleUploadedFile("report.pdf", b"%PDF-1.7\n")

        with self.assertRaisesMessage(
            ValidationError,
            "The uploaded file was flagged by malware scanning and was not saved.",
        ):
            scan_medical_report_file(uploaded_file)

    @patch("records.scanning._clamd_instream", side_effect=ConnectionRefusedError)
    def test_fails_closed_when_scanner_is_unavailable(self, scan_stream):
        uploaded_file = SimpleUploadedFile("report.pdf", b"%PDF-1.7\n")

        with self.assertRaisesMessage(
            ValidationError,
            "Report scanning is unavailable. Try again later.",
        ):
            scan_medical_report_file(uploaded_file)


class PrivateReportAccessTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.owner = user_model.objects.create_user(
            username="report-owner",
            password="test-password",
        )
        PatientProfile.objects.create(user=self.owner)
        self.other_patient = user_model.objects.create_user(
            username="other-patient",
            password="test-password",
        )
        PatientProfile.objects.create(user=self.other_patient)
        self.report = MedicalReport.objects.create(
            patient=self.owner,
            title="Sample lab report",
            file=SimpleUploadedFile(
                "report.pdf",
                b"non-sensitive test report",
                content_type="application/pdf",
            ),
        )

    def tearDown(self):
        self.report.file.delete(save=False)

    def test_only_owner_can_download_report(self):
        response = self.client.get(reverse("records:report_file", args=[self.report.pk]))
        self.assertEqual(response.status_code, 302)
        self.client.login(username="report-owner", password="test-password")
        response = self.client.get(reverse("records:report_file", args=[self.report.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Cache-Control"], "private, no-store")
        self.assertEqual(response["X-Content-Type-Options"], "nosniff")
        self.assertIn("attachment;", response["Content-Disposition"])
        self.assertEqual(b"".join(response.streaming_content), b"non-sensitive test report")

        self.client.logout()
        self.client.login(username="other-patient", password="test-password")
        response = self.client.get(reverse("records:report_file", args=[self.report.pk]))
        self.assertEqual(response.status_code, 404)

    def test_report_file_is_not_served_from_public_media_url(self):
        response = self.client.get(self.report.file.url)
        self.assertEqual(response.status_code, 404)

    def test_report_detail_is_scoped_to_owner(self):
        self.client.login(username="other-patient", password="test-password")
        response = self.client.get(reverse("records:report_detail", args=[self.report.pk]))
        self.assertEqual(response.status_code, 404)
