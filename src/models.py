"""Pydantic models for CV data validation."""

from pydantic import BaseModel, Field, field_validator


class CareerGrowthItem(BaseModel):
    """An internal role progression within the same company."""

    role: str
    start_date: str
    end_date: str
    summary: str = ""


class ExperienceItem(BaseModel):
    """A single professional experience entry."""

    company: str
    role: str
    start_date: str
    end_date: str
    employment_type: str = ""
    career_growth: list[CareerGrowthItem] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)

    @field_validator("responsibilities", mode="before")
    @classmethod
    def ensure_responsibilities_list(cls, value: object) -> list[str]:
        if value is None:
            return []
        if isinstance(value, list):
            return [str(item) for item in value]
        return [str(value)]


class EducationItem(BaseModel):
    """A single education entry."""

    institution: str
    degree: str
    field: str = ""
    start_date: str = ""
    end_date: str = ""


class LanguageItem(BaseModel):
    """A spoken language and proficiency level."""

    name: str
    level: str


class CVData(BaseModel):
    """Complete resume payload loaded from JSON."""

    name: str
    title: str
    subtitle: str = ""
    email: str
    phone: str = ""
    location: str = ""
    linkedin: str = ""
    github: str = ""
    summary: str = ""
    skills: dict[str, list[str]] = Field(default_factory=dict)
    experience: list[ExperienceItem] = Field(default_factory=list)
    education: list[EducationItem] = Field(default_factory=list)
    languages: list[LanguageItem] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)

    @field_validator("linkedin", "github", mode="before")
    @classmethod
    def normalize_optional_url(cls, value: object) -> str:
        if value is None:
            return ""
        return str(value).strip()

    @property
    def has_linkedin(self) -> bool:
        return bool(self.linkedin.strip())

    @property
    def has_github(self) -> bool:
        return bool(self.github.strip())

    @property
    def current_position(self) -> ExperienceItem | None:
        if not self.experience:
            return None
        return self.experience[0]

    @property
    def previous_experience(self) -> list[ExperienceItem]:
        if len(self.experience) <= 1:
            return []
        return self.experience[1:]

    def output_pdf_name(self) -> str:
        """Build a safe PDF filename from the person's name."""
        safe_name = "".join(
            char if char.isalnum() or char in (" ", "-", "_") else ""
            for char in self.name.strip()
        )
        parts = safe_name.split()
        formatted = "_".join(part.capitalize() for part in parts if part)
        return f"CV_{formatted or 'Resume'}.pdf"
