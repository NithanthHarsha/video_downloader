import re
import unicodedata
import os
import shutil
import logging
from pathlib import Path
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)

SAFE_CHARS_PATTERN = re.compile(r'[^a-zA-Z0-9_\-\. ]')

def sanitize_filename(filename: str, default: str = "download", max_length: int = 120) -> str:
    """
    Sanitizes a filename to prevent path traversal, null bytes,
    and reserved OS filenames.
    """
    if not filename:
        return f"{default}.mp4"

    filename = unicodedata.normalize('NFKD', filename)
    filename = Path(filename).name
    cleaned = SAFE_CHARS_PATTERN.sub('', filename).strip()

    if not cleaned:
        cleaned = default

    if len(cleaned) > max_length:
        base, ext = Path(cleaned).stem, Path(cleaned).suffix
        cleaned = f"{base[:max_length - len(ext)]}{ext}"

    reserved = {"CON", "PRN", "AUX", "NUL", "COM1", "COM2", "COM3", "COM4",
                "COM5", "COM6", "COM7", "COM8", "COM9", "LPT1", "LPT2",
                "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"}
    stem = Path(cleaned).stem.upper()
    if stem in reserved:
        cleaned = f"file_{cleaned}"

    return cleaned

def format_duration(seconds: int | float | None) -> str:
    """Formats duration in seconds into MM:SS or HH:MM:SS."""
    if not seconds or seconds <= 0:
        return "0:00"
    
    total_seconds = int(seconds)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60

    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"

def format_filesize(bytes_val: int | float | None) -> str:
    """Formats byte counts into human-readable strings like '24.5 MB'."""
    if not bytes_val or bytes_val <= 0:
        return "Unknown size"
    
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(bytes_val)
    unit_idx = 0
    while size >= 1024.0 and unit_idx < len(units) - 1:
        size /= 1024.0
        unit_idx += 1
    
    return f"{size:.1f} {units[unit_idx]}"

def cleanup_path(path_to_remove: Path | str | None):
    """Safely removes a temporary file or directory."""
    if not path_to_remove:
        return
    try:
        p = Path(path_to_remove)
        if p.exists():
            if p.is_dir():
                shutil.rmtree(p, ignore_errors=True)
            else:
                p.unlink(missing_ok=True)
            logger.info(f"Cleaned temporary path: {p}")
    except Exception as e:
        logger.warning(f"Failed to clean temporary path {path_to_remove}: {e}")

def get_client_ip(request) -> str:
    """Extracts client IP address considering reverse proxies."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '127.0.0.1')

def custom_exception_handler(exc, context):
    """
    Standardizes unhandled DRF exceptions into consistent JSON format:
    {"success": False, "error": {"code": "...", "message": "..."}}
    """
    response = exception_handler(exc, context)

    if response is not None:
        error_msg = "An error occurred."
        error_code = "API_ERROR"

        if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
            error_code = "RATE_LIMITED"
            error_msg = "Too many requests. Please wait a moment and try again."
        elif isinstance(response.data, dict):
            # Extract first error message
            for key, val in response.data.items():
                if isinstance(val, list) and val:
                    error_msg = f"{key}: {val[0]}"
                else:
                    error_msg = f"{key}: {val}"
                break
            error_code = "VALIDATION_ERROR"
        elif isinstance(response.data, list) and response.data:
            error_msg = str(response.data[0])
            error_code = "VALIDATION_ERROR"

        response.data = {
            "success": False,
            "error": {
                "code": error_code,
                "message": error_msg
            }
        }
    else:
        logger.error(f"Unhandled Exception: {exc}", exc_info=True)
        response = Response(
            {
                "success": False,
                "error": {
                    "code": "SERVER_ERROR",
                    "message": "An internal server error occurred. Please try again later."
                }
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return response
