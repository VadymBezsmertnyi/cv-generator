"""CV Generator — orchestrates data loading, HTML rendering, and PDF export."""

from __future__ import annotations

import sys
from pathlib import Path

from src.config import GeneratorConfig, ProjectPaths
from src.helpers import ensure_directory, load_cv_data
from src.html_renderer import HTMLRenderer
from src.pdf_generator import PDFGenerator


class CVGenerator:
    """High-level facade for generating a CV PDF from JSON data."""

    def __init__(self, config: GeneratorConfig) -> None:
        self._config = config
        self._paths = config.paths
        self._renderer = HTMLRenderer(self._paths.template_file.parent)
        self._pdf_generator = PDFGenerator()

    @classmethod
    def from_project_root(cls, root: Path | None = None) -> "CVGenerator":
        """Create a generator using default project paths."""
        paths = ProjectPaths.from_root(root)
        config = GeneratorConfig(paths=paths)
        return cls(config)

    def generate(self) -> Path:
        """Load data, render HTML, and write the PDF to the output directory."""
        paths = self._paths

        if not paths.data_file.is_file():
            raise FileNotFoundError(f"CV data file not found: {paths.data_file}")

        cv = load_cv_data(paths.data_file)
        ensure_directory(paths.output_dir)

        html = self._renderer.render_cv(
            cv,
            template_name=paths.template_file.name,
            photo_path=paths.photo_file,
            styles_path=paths.styles_file,
            icons_dir=paths.icons_dir,
        )

        output_path = paths.output_dir / cv.output_pdf_name()
        self._pdf_generator.generate_from_html(html, output_path)
        return output_path


def main() -> int:
    """Entry point for `python generate_cv.py`."""
    try:
        generator = CVGenerator.from_project_root()
        output_path = generator.generate()
        print(f"CV generated successfully: {output_path}")
        return 0
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Failed to generate CV: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
