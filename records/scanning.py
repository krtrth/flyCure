import logging
import socket
import struct

from django.conf import settings
from django.core.exceptions import ValidationError


logger = logging.getLogger(__name__)


class ClamAVProtocolError(Exception):
    pass


def scan_medical_report_file(uploaded_file):
    try:
        response = _clamd_instream(uploaded_file)
    except (OSError, ClamAVProtocolError) as exc:
        logger.exception("ClamAV scan failed; rejecting report upload.")
        raise ValidationError(
            "Report scanning is unavailable. Try again later."
        ) from exc
    finally:
        uploaded_file.seek(0)

    if response == "stream: OK":
        return
    if response.startswith("stream: ") and response.endswith(" FOUND"):
        logger.warning("ClamAV flagged a report upload; rejecting the file.")
        raise ValidationError("The uploaded file was flagged by malware scanning and was not saved.")

    logger.error("ClamAV returned an unsuccessful scan response; rejecting report upload.")
    raise ValidationError("The report could not be scanned. Try again later.")


def _clamd_instream(uploaded_file):
    with socket.create_connection(
        (settings.CLAMAV_HOST, settings.CLAMAV_PORT),
        timeout=settings.CLAMAV_SCAN_TIMEOUT_SECONDS,
    ) as connection:
        connection.settimeout(settings.CLAMAV_SCAN_TIMEOUT_SECONDS)
        connection.sendall(b"zINSTREAM\x00")
        uploaded_file.seek(0)
        while chunk := uploaded_file.read(64 * 1024):
            connection.sendall(struct.pack("!I", len(chunk)))
            connection.sendall(chunk)
        connection.sendall(struct.pack("!I", 0))
        return _read_clamd_response(connection)


def _read_clamd_response(connection):
    response = bytearray()
    while len(response) <= 4096:
        chunk = connection.recv(1024)
        if not chunk:
            raise ClamAVProtocolError("ClamAV closed the connection without a response.")
        response.extend(chunk)
        if b"\x00" in response:
            message = bytes(response).split(b"\x00", maxsplit=1)[0]
            try:
                return message.decode("ascii")
            except UnicodeDecodeError as exc:
                raise ClamAVProtocolError("ClamAV returned a non-ASCII response.") from exc
    raise ClamAVProtocolError("ClamAV response exceeded the expected size.")
