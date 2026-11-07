from flask import Flask, request, send_file, jsonify
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from io import BytesIO
import re

app = Flask(__name__)

SECTION_HEADINGS = {
    "PROFESSIONAL SUMMARY",
    "SUMMARY",
    "PROFILE",
    "EDUCATION",
    "WORK EXPERIENCE",
    "EXPERIENCE",
    "EMPLOYMENT",
    "SKILLS",
    "TECHNICAL SKILLS",
    "PROJECTS",
    "CERTIFICATIONS",
    "CERTIFICATES",
    "ACHIEVEMENTS",
    "LANGUAGES",
    "VOLUNTEER EXPERIENCE",
    "COURSES",
    "INTERESTS",
}

def clean_markdown(text):
    """Remove common Markdown markers while preserving the actual CV text."""
    text = text.strip()
    text = re.sub(r"^\s{0,3}#{1,6}\s*", "", text)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    text = re.sub(r"(?<!\*)\*(?!\s)(.*?)(?<!\s)\*(?!\*)", r"\1", text)
    text = re.sub(r"(?<!_)_(?!\s)(.*?)(?<!\s)_(?!_)", r"\1", text)
    return text.strip()

def add_formatted_paragraph(document, raw_line, first_content_line=False):
    line = raw_line.strip()

    if not line:
        document.add_paragraph()
        return

    # Markdown headings such as ## EDUCATION or **EDUCATION**
    heading_text = clean_markdown(line)
    normalized = heading_text.upper().strip().rstrip(":")

    if normalized in SECTION_HEADINGS:
        p = document.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(normalized)
        run.bold = True
        run.font.name = "Arial"
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(31, 78, 121)
        return

    # The first non-empty line is treated as the candidate's name.
    if first_content_line:
        p = document.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(heading_text)
        run.bold = True
        run.font.name = "Arial"
        run.font.size = Pt(20)
        run.font.color.rgb = RGBColor(31, 78, 121)
        return

    # Contact details often appear immediately below the name.
    if ("@" in line or "|" in line) and len(line) < 180:
        p = document.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(8)
        run = p.add_run(heading_text)
        run.font.name = "Arial"
        run.font.size = Pt(9)
        run.font.color.rgb = RGBColor(89, 89, 89)
        return

    # Regular text: strip Markdown and keep a readable ATS-friendly paragraph.
    p = document.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.08

    # Handle simple Markdown bullet points.
    if line.startswith(("- ", "* ", "• ")):
        clean_line = clean_markdown(line[2:])
        p.style = document.styles["List Bullet"]
        run = p.add_run(clean_line)
    else:
        # Bold text such as **Bachelor of Computer Science** is kept bold.
        match = re.match(r"^\*\*(.+?)\*\*(.*)$", line)
        if match:
            first = p.add_run(match.group(1))
            first.bold = True
            p.add_run(clean_markdown(match.group(2)))
        else:
            p.add_run(heading_text)

    for run in p.runs:
        run.font.name = "Arial"
        run.font.size = Pt(10)

@app.route("/create-cv", methods=["POST"])
def create_cv():
    data = request.get_json(silent=True) or {}
    cv_text = data.get("cv_text", "").strip()

    if not cv_text:
        return jsonify({"error": "CV text is required"}), 400

    document = Document()
    section = document.sections[0]
    section.top_margin = Inches(0.65)
    section.bottom_margin = Inches(0.65)
    section.left_margin = Inches(0.75)
    section.right_margin = Inches(0.75)

    # Set a consistent default font.
    normal_style = document.styles["Normal"]
    normal_style.font.name = "Arial"
    normal_style.font.size = Pt(10)

    non_empty_seen = False
    for raw_line in cv_text.splitlines():
        is_first_content_line = bool(raw_line.strip()) and not non_empty_seen
        add_formatted_paragraph(document, raw_line, is_first_content_line)
        if raw_line.strip():
            non_empty_seen = True

    file_buffer = BytesIO()
    document.save(file_buffer)
    file_buffer.seek(0)

    return send_file(
        file_buffer,
        as_attachment=True,
        download_name="CareerCanvas.docx",
        mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False)
