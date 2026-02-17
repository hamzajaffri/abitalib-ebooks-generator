"""PDF export engine for multi-chapter books."""

from __future__ import annotations

from pathlib import Path
from typing import List

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from config import PDF_BODY_FONT_SIZE, PDF_FONT_NAME, PDF_TITLE_FONT_SIZE



def export_pdf(title: str, author: str, toc_text: str, chapters: List[str], chapter_titles: List[str], output_path: Path) -> Path:
    """Export book content to a multi-page PDF document."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pdf = canvas.Canvas(str(output_path), pagesize=A4)
    width, height = A4

    pdf.setFont(PDF_FONT_NAME, PDF_TITLE_FONT_SIZE)
    pdf.drawString(72, height - 72, title)
    pdf.setFont(PDF_FONT_NAME, 14)
    pdf.drawString(72, height - 100, f"Author: {author}")
    pdf.showPage()

    pdf.setFont(PDF_FONT_NAME, 16)
    pdf.drawString(72, height - 72, "Table of Contents")
    pdf.setFont(PDF_FONT_NAME, PDF_BODY_FONT_SIZE)
    y = height - 100
    for line in toc_text.splitlines():
        pdf.drawString(72, y, line)
        y -= 16
        if y < 72:
            pdf.showPage()
            y = height - 72
    pdf.showPage()

    for idx, chapter in enumerate(chapters):
        chapter_title = chapter_titles[idx]
        pdf.setFont(PDF_FONT_NAME, 16)
        pdf.drawString(72, height - 72, chapter_title)
        y = height - 100
        pdf.setFont(PDF_FONT_NAME, PDF_BODY_FONT_SIZE)

        for paragraph in chapter.split("\n"):
            words = paragraph.split()
            line = ""
            for word in words:
                candidate = f"{line} {word}".strip()
                if pdf.stringWidth(candidate, PDF_FONT_NAME, PDF_BODY_FONT_SIZE) > width - 144:
                    pdf.drawString(72, y, line)
                    y -= 16
                    line = word
                else:
                    line = candidate
                if y < 72:
                    pdf.showPage()
                    pdf.setFont(PDF_FONT_NAME, PDF_BODY_FONT_SIZE)
                    y = height - 72
            if line:
                pdf.drawString(72, y, line)
                y -= 16
            y -= 6
            if y < 72:
                pdf.showPage()
                pdf.setFont(PDF_FONT_NAME, PDF_BODY_FONT_SIZE)
                y = height - 72
        pdf.showPage()

    pdf.save()
    return output_path
