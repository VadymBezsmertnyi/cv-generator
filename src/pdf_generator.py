"""Playwright-based HTML to PDF conversion."""

from pathlib import Path

from playwright.sync_api import sync_playwright

from src.constants import PDF_FORMAT, PDF_MARGIN_MM, PDF_PRINT_BACKGROUND


class PDFGenerator:
    """Convert rendered HTML into a print-ready PDF."""

    def __init__(
        self,
        *,
        page_format: str = PDF_FORMAT,
        margin: str = PDF_MARGIN_MM,
        print_background: bool = PDF_PRINT_BACKGROUND,
    ) -> None:
        self._page_format = page_format
        self._margin = margin
        self._print_background = print_background

    def generate_from_html(self, html: str, output_path: Path) -> Path:
        """Render HTML string to a PDF file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            try:
                page = browser.new_page()
                page.set_content(html, wait_until="networkidle")
                page.pdf(
                    path=str(output_path),
                    format=self._page_format,
                    margin={
                        "top": self._margin,
                        "right": self._margin,
                        "bottom": self._margin,
                        "left": self._margin,
                    },
                    print_background=self._print_background,
                )
            finally:
                browser.close()

        return output_path

    def generate_from_file(self, html_file: Path, output_path: Path) -> Path:
        """Render an HTML file to a PDF file."""
        html = html_file.read_text(encoding="utf-8")
        return self.generate_from_html(html, output_path)
