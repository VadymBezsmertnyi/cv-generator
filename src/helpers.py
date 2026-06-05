"""Shared utility functions."""

import base64
import json
import re
from pathlib import Path

from src.models import CVData


def load_cv_data(data_file: Path) -> CVData:
    """Load and validate CV JSON from disk."""
    raw = json.loads(data_file.read_text(encoding="utf-8"))
    return CVData.model_validate(raw)


def ensure_directory(directory: Path) -> Path:
    """Create a directory if it does not exist."""
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def file_to_data_uri(file_path: Path, mime_type: str) -> str | None:
    """Encode a file as a data URI, or return None if the file is missing."""
    if not file_path.is_file():
        return None
    encoded = base64.b64encode(file_path.read_bytes()).decode("ascii")
    return f"data:{mime_type};base64,{encoded}"


def photo_to_data_uri(photo_path: Path) -> str | None:
    """Convert a profile photo to a JPEG data URI."""
    if not photo_path.is_file():
        return None

    suffix = photo_path.suffix.lower()
    mime_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
    }
    mime_type = mime_map.get(suffix, "image/jpeg")
    return file_to_data_uri(photo_path, mime_type)


def svg_to_data_uri(svg_path: Path) -> str | None:
    """Convert an SVG icon to a data URI."""
    return file_to_data_uri(svg_path, "image/svg+xml")


def load_icon_data_uris(icons_dir: Path, icon_names: dict[str, str]) -> dict[str, str | None]:
    """Load contact icons as data URIs keyed by logical name."""
    return {
        key: svg_to_data_uri(icons_dir / filename)
        for key, filename in icon_names.items()
    }


def inline_styles(styles_file: Path) -> str:
    """Read CSS content for embedding in HTML."""
    return styles_file.read_text(encoding="utf-8")


def format_date_range(start_date: str, end_date: str) -> str:
    """Format an experience date range for display."""
    start = start_date.strip()
    end = end_date.strip() or "Present"
    if start and end:
        return f"{start} — {end}"
    return start or end


def strip_url_prefix(url: str) -> str:
    """Remove protocol and www prefix for compact link display."""
    cleaned = url.strip()
    cleaned = re.sub(r"^https?://", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"^www\.", "", cleaned, flags=re.IGNORECASE)
    return cleaned.rstrip("/")
