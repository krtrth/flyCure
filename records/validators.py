from pathlib import Path
from zipfile import BadZipFile, ZipFile

from django.conf import settings
from django.core.exceptions import ValidationError

from .scanning import scan_medical_report_file


REPORT_FILE_MIME_TYPES = {
    ".pdf": {"application/pdf"},
    ".jpg": {"image/jpeg"},
    ".jpeg": {"image/jpeg"},
    ".png": {"image/png"},
    ".docx": {
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    },
}


def validate_medical_report_file(uploaded_file):
    suffix = Path(uploaded_file.name).suffix.lower()
    allowed_mime_types = REPORT_FILE_MIME_TYPES.get(suffix)
    if allowed_mime_types is None:
        raise ValidationError("Upload a PDF, JPEG, PNG, or DOCX file.")

    maximum_size = settings.MAX_REPORT_UPLOAD_SIZE_MB * 1024 * 1024
    if uploaded_file.size > maximum_size:
        raise ValidationError(
            f"The file must be no larger than {settings.MAX_REPORT_UPLOAD_SIZE_MB} MB."
        )

    content_type = getattr(uploaded_file, "content_type", None)
    if content_type and content_type not in allowed_mime_types:
        raise ValidationError("The file's content type does not match its extension.")

    try:
        uploaded_file.seek(0)
        signature = uploaded_file.read(8)
        if suffix == ".pdf" and not signature.startswith(b"%PDF-"):
            raise ValidationError("The uploaded file is not a valid PDF.")
        if suffix in {".jpg", ".jpeg"} and not signature.startswith(b"\xff\xd8\xff"):
            raise ValidationError("The uploaded file is not a valid JPEG image.")
        if suffix == ".png" and signature != b"\x89PNG\r\n\x1a\n":
            raise ValidationError("The uploaded file is not a valid PNG image.")
        if suffix == ".docx":
            _validate_docx(uploaded_file, signature)
    finally:
        uploaded_file.seek(0)

    scan_medical_report_file(uploaded_file)


def _validate_docx(uploaded_file, signature):
    if not signature.startswith(b"PK\x03\x04"):
        raise ValidationError("The uploaded file is not a valid DOCX document.")
    try:
        with ZipFile(uploaded_file) as archive:
            members = set(archive.namelist())
    except (BadZipFile, OSError) as exc:
        raise ValidationError("The uploaded file is not a valid DOCX document.") from exc

    if not {"[Content_Types].xml", "word/document.xml"}.issubset(members):
        raise ValidationError("The uploaded file is not a valid DOCX document.")
