"""Jinja2 HTML rendering for CV templates."""

from dataclasses import dataclass
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.constants import CONTACT_ICONS, SKILL_GROUPS
from src.helpers import (
    format_date_range,
    inline_styles,
    load_icon_data_uris,
    photo_to_data_uri,
    strip_url_prefix,
)
from src.models import CVData


@dataclass(frozen=True)
class RenderContext:
    """Template context passed to Jinja2."""

    cv: CVData
    photo_data_uri: str | None
    icons: dict[str, str | None]
    styles: str
    skill_groups: tuple[str, ...]


class HTMLRenderer:
    """Render CV data into HTML using Jinja2 templates."""

    def __init__(self, templates_dir: Path) -> None:
        self._templates_dir = templates_dir
        self._env = Environment(
            loader=FileSystemLoader(str(templates_dir)),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self._register_filters()

    def _register_filters(self) -> None:
        self._env.filters["date_range"] = format_date_range
        self._env.filters["strip_url"] = strip_url_prefix

    def build_context(
        self,
        cv: CVData,
        *,
        photo_path: Path,
        styles_path: Path,
        icons_dir: Path,
    ) -> RenderContext:
        """Assemble all template variables for a render pass."""
        return RenderContext(
            cv=cv,
            photo_data_uri=photo_to_data_uri(photo_path),
            icons=load_icon_data_uris(icons_dir, CONTACT_ICONS),
            styles=inline_styles(styles_path),
            skill_groups=SKILL_GROUPS,
        )

    def render(
        self,
        template_name: str,
        context: RenderContext,
    ) -> str:
        """Render a named template with the given context."""
        template = self._env.get_template(template_name)
        return template.render(
            cv=context.cv,
            photo=context.photo_data_uri,
            icons=context.icons,
            styles=context.styles,
            skill_groups=context.skill_groups,
        )

    def render_cv(
        self,
        cv: CVData,
        *,
        template_name: str,
        photo_path: Path,
        styles_path: Path,
        icons_dir: Path,
    ) -> str:
        """Convenience method: build context and render in one step."""
        context = self.build_context(
            cv,
            photo_path=photo_path,
            styles_path=styles_path,
            icons_dir=icons_dir,
        )
        return self.render(template_name, context)
