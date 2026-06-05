"""Path and runtime configuration."""

from dataclasses import dataclass
from pathlib import Path

from src.constants import (
    DEFAULT_DATA_FILE,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_PHOTO_FILE,
    DEFAULT_STYLES,
    DEFAULT_TEMPLATE,
    DEFAULT_TEMPLATE_ID,
)


@dataclass(frozen=True)
class ProjectPaths:
    """Resolved, cross-platform project paths."""

    root: Path
    data_file: Path
    photo_file: Path
    template_file: Path
    styles_file: Path
    icons_dir: Path
    output_dir: Path

    @classmethod
    def from_root(
        cls,
        root: Path | None = None,
        *,
        data_file: str = DEFAULT_DATA_FILE,
        photo_file: str = DEFAULT_PHOTO_FILE,
        template_file: str = DEFAULT_TEMPLATE,
        styles_file: str = DEFAULT_STYLES,
        output_dir: str = DEFAULT_OUTPUT_DIR,
    ) -> "ProjectPaths":
        """Build paths from the project root directory."""
        resolved_root = (root or _detect_project_root()).resolve()
        return cls(
            root=resolved_root,
            data_file=resolved_root / data_file,
            photo_file=resolved_root / photo_file,
            template_file=resolved_root / template_file,
            styles_file=resolved_root / styles_file,
            icons_dir=resolved_root / "assets" / "icons",
            output_dir=resolved_root / output_dir,
        )


@dataclass(frozen=True)
class GeneratorConfig:
    """Runtime configuration for a single CV generation run."""

    paths: ProjectPaths
    template_id: str = DEFAULT_TEMPLATE_ID
    profile_name: str | None = None  # Reserved for future multi-profile support.

    @property
    def output_filename(self) -> str:
        """Placeholder; actual filename is derived from CV data at runtime."""
        return "CV.pdf"


def _detect_project_root() -> Path:
    """Locate project root as the parent of the src package."""
    return Path(__file__).resolve().parent.parent
