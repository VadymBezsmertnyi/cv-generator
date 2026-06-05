"""Application-wide constants."""

from pathlib import Path

# Skill groups displayed in fixed order on page 1.
SKILL_GROUPS: tuple[str, ...] = (
    "Frontend",
    "Mobile",
    "Backend",
    "Databases",
    "Cloud & DevOps",
    "AI & Automation",
    "Testing",
)

# Contact icon filenames (stored under assets/icons/).
CONTACT_ICONS: dict[str, str] = {
    "location": "location.svg",
    "phone": "phone.svg",
    "email": "email.svg",
    "github": "github.svg",
    "linkedin": "linkedin.svg",
}

# PDF generation defaults.
PDF_FORMAT: str = "A4"
PDF_MARGIN_MM: str = "12mm"
PDF_PRINT_BACKGROUND: bool = True

# Default paths relative to project root.
DEFAULT_DATA_FILE: str = "data/cv.json"
DEFAULT_PHOTO_FILE: str = "data/photo.jpg"
DEFAULT_TEMPLATE: str = "templates/cv_template.html"
DEFAULT_STYLES: str = "templates/styles.css"
DEFAULT_OUTPUT_DIR: str = "output"

# Template identifiers for future multi-template support.
DEFAULT_TEMPLATE_ID: str = "default"
