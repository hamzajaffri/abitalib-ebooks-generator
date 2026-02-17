"""Gradio user interface for ABITALIB E-Books Generator."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import gradio as gr

from book_engine import BookEngine, BookRequest
from config import MAX_AUTHOR_LENGTH, MAX_CHAPTERS, MAX_TITLE_LENGTH, MIN_CHAPTERS, OUTPUT_DIR
from epub_engine import export_epub
from hardware import hardware_as_dict
from isbn import create_isbn_barcode, generate_sample_isbn
from license import generate_publishing_license
from metadata import generate_metadata
from model_loader import LocalModelLoader
from pdf_engine import export_pdf
from toc import create_toc


LOADER = LocalModelLoader()
ENGINE = BookEngine(LOADER)



def _format_hardware() -> str:
    """Format hardware data for UI display."""
    hw = hardware_as_dict()
    return "\n".join([f"{k}: {v}" for k, v in hw.items()])



def load_model(model_file: Optional[str]) -> str:
    """Load selected GGUF model and return status text."""
    try:
        if not model_file:
            return "Please provide a GGUF model path first."
        LOADER.load_model(model_file)
        return f"Model loaded successfully: {model_file}"
    except Exception as exc:
        return f"Model load failed: {exc}"



def generate_book_package(
    title: str,
    author: str,
    genre: str,
    language: str,
    chapter_count: int,
    output_dir: str,
) -> tuple[str, str, str, str, str]:
    """Generate content and export artifacts, returning status and file paths."""
    try:
        title = title.strip()[:MAX_TITLE_LENGTH]
        author = author.strip()[:MAX_AUTHOR_LENGTH]
        chapter_count = max(MIN_CHAPTERS, min(MAX_CHAPTERS, int(chapter_count)))

        out_dir = Path(output_dir).expanduser().resolve() if output_dir else OUTPUT_DIR
        out_dir.mkdir(parents=True, exist_ok=True)

        request = BookRequest(
            title=title,
            author=author,
            genre=genre,
            language=language,
            chapter_count=chapter_count,
        )

        chapter_titles, chapters, _memory = ENGINE.generate_book(request)
        toc_text = create_toc(chapter_titles)
        metadata = generate_metadata(title, author, genre, language)

        pdf_path = export_pdf(title, author, toc_text, chapters, chapter_titles, out_dir / f"{title}.pdf")
        epub_path = export_epub(metadata, chapter_titles, chapters, out_dir / f"{title}.epub")
        isbn_value = generate_sample_isbn()
        isbn_path = create_isbn_barcode(isbn_value, out_dir)
        license_path = generate_publishing_license(title, author, isbn_value, out_dir)

        preview = "\n\n".join(chapters[:2])
        status = "Generation complete. Files saved successfully."
        return status, str(pdf_path), str(epub_path), str(isbn_path), f"{license_path}\n\nPreview:\n{preview}"

    except Exception as exc:
        return f"Generation failed: {exc}", "", "", "", ""



def build_ui() -> gr.Blocks:
    """Construct and return the Gradio Blocks interface."""
    with gr.Blocks(title="ABITALIB E-Books Generator") as app:
        gr.Markdown("# ABITALIB E-Books Generator™")
        gr.Markdown("Generate full multi-chapter books locally with GGUF models.")

        with gr.Tab("System"):
            hardware_box = gr.Textbox(label="Detected Hardware", value=_format_hardware(), lines=10)
            _ = hardware_box

        with gr.Tab("Model"):
            model_path_input = gr.Textbox(label="GGUF Model Path", placeholder="/path/to/model.gguf")
            load_button = gr.Button("Load Model")
            model_status = gr.Textbox(label="Model Status", lines=2)
            load_button.click(load_model, inputs=[model_path_input], outputs=[model_status])

        with gr.Tab("Generate Book"):
            title = gr.Textbox(label="Book Title", value="Echoes of Tomorrow")
            author = gr.Textbox(label="Author", value="ABITALIB")
            genre = gr.Dropdown(["Sci-Fi", "Fantasy", "Mystery", "Romance", "Business"], value="Sci-Fi", label="Genre")
            language = gr.Dropdown(["English", "French", "Spanish", "Arabic"], value="English", label="Language")
            chapter_count = gr.Slider(minimum=1, maximum=20, step=1, value=6, label="Chapter Count")
            output_dir = gr.Textbox(label="Output Directory", value=str(OUTPUT_DIR))

            generate_btn = gr.Button("Generate Book + PDF + EPUB")
            status = gr.Textbox(label="Status")
            pdf_file = gr.Textbox(label="PDF Path")
            epub_file = gr.Textbox(label="EPUB Path")
            isbn_file = gr.Textbox(label="ISBN Barcode Path")
            details = gr.Textbox(label="License + Preview", lines=12)

            generate_btn.click(
                generate_book_package,
                inputs=[title, author, genre, language, chapter_count, output_dir],
                outputs=[status, pdf_file, epub_file, isbn_file, details],
            )

    return app


if __name__ == "__main__":
    build_ui().launch(server_name="0.0.0.0", server_port=7860)
