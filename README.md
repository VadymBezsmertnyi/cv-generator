# CV Generator

Generate modern, ATS-friendly PDF resumes from JSON data using HTML templates, Jinja2, and Playwright.

## Features

- **JSON-driven** — all resume content lives in `data/cv.json`
- **Validated** — Pydantic models enforce a consistent data schema
- **Template-based** — Jinja2 HTML templates with embedded CSS
- **High-quality PDF** — rendered via Playwright (Chromium)
- **Cross-platform** — paths use `pathlib` (macOS, Windows, Linux)
- **Graceful fallbacks** — missing photo or social links are hidden automatically
- **Extensible** — architecture supports multiple templates and profiles in the future

## Project Structure

```text
cv-generator/
├── data/
│   ├── cv.json          # Resume data
│   └── photo.jpg        # Profile photo (optional)
├── assets/icons/        # Contact SVG icons
├── templates/
│   ├── cv_template.html
│   └── styles.css
├── output/              # Generated PDFs
├── src/                 # Application source
├── generate_cv.py       # CLI entry point
└── requirements.txt
```

## Requirements

- Python 3.12+
- pip

## Setup

1. **Clone or navigate to the project directory:**

   ```bash
   cd cv-generator
   ```

2. **Create and activate a virtual environment (recommended):**

   ```bash
   python3 -m venv .venv

   # macOS / Linux
   source .venv/bin/activate

   # Windows
   .venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers (one-time setup):**

   ```bash
   python -m playwright install chromium
   ```

## Usage

1. Edit `data/cv.json` with your resume information.
2. Optionally replace `data/photo.jpg` with your profile photo.
3. Run the generator:

   ```bash
   python generate_cv.py
   ```

4. Find the output PDF at:

   ```text
   output/CV_Vadym_Bezsmertnyi.pdf
   ```

   The filename is derived automatically from the `name` field in your JSON.

## Data Schema

```json
{
  "name": "",
  "title": "",
  "subtitle": "",
  "email": "",
  "phone": "",
  "location": "",
  "linkedin": "",
  "github": "",
  "summary": "",
  "skills": {},
  "experience": [],
  "education": [],
  "languages": [],
  "certifications": []
}
```

### Experience entry

```json
{
  "company": "Company Name",
  "role": "Job Title",
  "start_date": "Jan 2024",
  "end_date": "Present",
  "responsibilities": ["Achievement one", "Achievement two"]
}
```

### Skills

Skills are grouped by category. Standard groups (in display order):

- Frontend
- Mobile
- Backend
- Databases
- Cloud & DevOps
- AI & Automation
- Testing

Additional custom groups in `skills` are rendered after the standard ones.

## Resume Layout

**Page 1:** Header (name, title, subtitle, photo), Contact, Professional Summary, Technical Skills, Current Position

**Page 2:** Professional Experience (timeline), Education, Languages, Certifications & Tools

## Optional Fields

| Field      | Behavior if missing        |
|------------|----------------------------|
| `photo.jpg`| Photo block hidden         |
| `linkedin` | LinkedIn icon/link hidden  |
| `github`   | GitHub icon/link hidden    |
| `subtitle` | Subtitle line hidden       |

## Troubleshooting

**`playwright install` not found**

Make sure Playwright is installed via pip, then run:

```bash
python -m playwright install chromium
```

**PDF is blank or missing styles**

Ensure `templates/styles.css` exists and Playwright Chromium is installed.

**Import errors**

Run commands from the project root directory where `generate_cv.py` is located.

## License

MIT
