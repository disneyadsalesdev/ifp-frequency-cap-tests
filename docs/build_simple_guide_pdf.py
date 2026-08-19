"""Build NEW-USER-SIMPLE-GUIDE.pdf from docs/source markdown (trainers edit source, share PDF)."""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent
SOURCE = DOCS / "source" / "NEW-USER-SIMPLE-GUIDE.md"
DEFAULT_PDF = DOCS / "NEW-USER-SIMPLE-GUIDE.pdf"
DEFAULT_HTML = DOCS / "NEW-USER-SIMPLE-GUIDE.html"

PRINT_CSS = """
@page { size: letter; margin: 0.75in; }
body {
  font-family: Segoe UI, Helvetica, Arial, sans-serif;
  font-size: 11pt;
  line-height: 1.45;
  color: #1e293b;
}
h1 { font-size: 18pt; color: #1e3a8a; margin-top: 0.8em; page-break-before: always; }
h1:first-of-type { page-break-before: avoid; font-size: 22pt; }
h2 { font-size: 13pt; color: #1e40af; margin-top: 1em; }
h3 { font-size: 11pt; color: #334155; margin-top: 0.8em; }
.part-banner {
  background: #dbeafe;
  border: 2px solid #1e40af;
  padding: 10px 12px;
  margin: 1em 0;
  font-size: 11pt;
}
ul, ol { margin: 0.4em 0; }
li { margin: 0.25em 0; }
code, pre { font-family: Consolas, monospace; font-size: 9pt; }
pre {
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  padding: 8px 10px;
  white-space: pre-wrap;
  word-wrap: break-word;
}
table { border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 10pt; }
th, td { border: 1px solid #cbd5e1; padding: 6px 8px; text-align: left; }
th { background: #dbeafe; }
hr { border: none; border-top: 1px solid #e2e8f0; margin: 1.5em 0; }
a { color: #1d4ed8; }
.cover-note { font-size: 10pt; color: #64748b; margin-bottom: 1.5em; }
"""


def ensure_packages() -> None:
    try:
        import markdown  # noqa: F401
        import xhtml2pdf  # noqa: F401
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "markdown", "xhtml2pdf", "--quiet"]
        )


def md_to_html(md_text: str) -> str:
    import markdown

    body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "nl2br"],
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>New User Guide — Cursor + IFP</title>
<style>{PRINT_CSS}</style>
</head>
<body>
<p class="cover-note">Internal — RYM onboarding. Share this PDF with new hires (not the source file).</p>
{body}
</body>
</html>"""


def html_to_pdf(html: str, pdf_path: Path) -> None:
    from xhtml2pdf import pisa

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    with pdf_path.open("wb") as out:
        status = pisa.CreatePDF(html.encode("utf-8"), dest=out, encoding="utf-8")
    if status.err:
        raise RuntimeError(f"PDF generation failed ({status.err} errors)")


def try_pandoc(md_path: Path, pdf_path: Path) -> bool:
    pandoc = shutil.which("pandoc")
    if not pandoc:
        return False
    cmd = [
        pandoc,
        str(md_path),
        "-o",
        str(pdf_path),
        "--pdf-engine=wkhtmltopdf",
        "-V",
        "geometry:margin=0.75in",
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def build(pdf_path: Path, html_path: Path | None, md_path: Path) -> Path:
    if not md_path.is_file():
        raise FileNotFoundError(f"Source not found: {md_path}")

    md_text = md_path.read_text(encoding="utf-8")

    if try_pandoc(md_path, pdf_path):
        return pdf_path

    ensure_packages()
    html = md_to_html(md_text)
    if html_path:
        html_path.write_text(html, encoding="utf-8")
    html_to_pdf(html, pdf_path)
    return pdf_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Build new-user simple guide PDF.")
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--html", type=Path, default=DEFAULT_HTML, help="Also write HTML (debug/print)")
    parser.add_argument("--source", type=Path, default=SOURCE)
    parser.add_argument("--no-html", action="store_true")
    args = parser.parse_args()

    pdf = build(
        args.output.resolve(),
        None if args.no_html else args.html.resolve(),
        args.source.resolve(),
    )
    print(f"Created: {pdf} ({pdf.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
