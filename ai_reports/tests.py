from django.test import SimpleTestCase, override_settings

from records.models import MedicalReport

from .services import generate_explanation


class ReportExplanationTests(SimpleTestCase):
    @override_settings(OPENAI_API_KEY="configured-but-unused", AI_REPORT_MODEL="example-model")
    def test_configured_api_key_does_not_mislabel_stub_output(self):
        explanation = generate_explanation(MedicalReport(title="Sample report"))

        self.assertEqual(explanation["model_name"], "local-stub")
        self.assertIn("development stub", explanation["patient_friendly_notes"])
