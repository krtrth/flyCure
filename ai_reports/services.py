"""AI explanation stubs for uploaded medical reports.

Without OPENAI_API_KEY, a deterministic local stub explanation is generated
so the patient flow works in development.
"""

from __future__ import annotations

from django.conf import settings

from records.models import MedicalReport

from .models import ReportExplanation


def queue_report_explanation(report: MedicalReport, force: bool = False) -> ReportExplanation:
    explanation, _created = ReportExplanation.objects.get_or_create(report=report)
    if explanation.status == ReportExplanation.Status.COMPLETE and not force:
        return explanation

    report.status = MedicalReport.Status.PROCESSING
    report.save(update_fields=["status", "updated_at"])

    explanation.status = ReportExplanation.Status.PENDING
    explanation.error_message = ""
    explanation.save(update_fields=["status", "error_message", "updated_at"])

    try:
        payload = generate_explanation(report)
        explanation.summary = payload["summary"]
        explanation.key_findings = payload["key_findings"]
        explanation.patient_friendly_notes = payload["patient_friendly_notes"]
        explanation.model_name = payload["model_name"]
        explanation.status = ReportExplanation.Status.COMPLETE
        explanation.save()
        report.status = MedicalReport.Status.READY
        report.save(update_fields=["status", "updated_at"])
    except Exception as exc:  # noqa: BLE001 - surface failure to patient UI
        explanation.status = ReportExplanation.Status.FAILED
        explanation.error_message = str(exc)
        explanation.save(update_fields=["status", "error_message", "updated_at"])
        report.status = MedicalReport.Status.FAILED
        report.save(update_fields=["status", "updated_at"])

    return explanation


def generate_explanation(report: MedicalReport) -> dict[str, str]:
    """Return explanation content.

    Hook point for a real LLM call when OPENAI_API_KEY is configured.
    """
    if settings.OPENAI_API_KEY:
        # Placeholder for a future OpenAI/Anthropic/Gemini integration.
        # Keeping the stub path until API credentials and document parsing
        # (PDF/OCR) are wired in a follow-up.
        return _stub_explanation(report, model_name=settings.AI_REPORT_MODEL)

    return _stub_explanation(report, model_name="local-stub")


def _stub_explanation(report: MedicalReport, model_name: str) -> dict[str, str]:
    need = report.treatment_need or "general care"
    return {
        "summary": (
            f"FlyCure reviewed “{report.title}” for a patient exploring {need} "
            "options in India. The file is stored privately on the patient account "
            "and can be shared with a coordinator after consent."
        ),
        "key_findings": (
            "- Document received and linked to the patient profile\n"
            f"- Stated treatment need: {need}\n"
            "- Recommended next step: coordinator review + hospital shortlist\n"
            "- No public pricing is generated from this file"
        ),
        "patient_friendly_notes": (
            "This is a development stub explanation. When an AI API key is configured, "
            "FlyCure will generate a clearer plain-language summary of lab values, "
            "imaging impressions, and questions to ask a specialist. Always confirm "
            "any interpretation with a licensed doctor before travel or treatment."
        ),
        "model_name": model_name,
    }
