"""EPUB export engine for generated books."""

from __future__ import annotations

from pathlib import Path
from typing import List

from ebooklib import epub

from metadata import BookMetadata



def export_epub(metadata: BookMetadata, chapter_titles: List[str], chapters: List[str], output_path: Path) -> Path:
    """Create and write an EPUB file with chapter navigation."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    book = epub.EpubBook()
    book.set_identifier(f"abitalib-{metadata.title.lower().replace(' ', '-')}")
    book.set_title(metadata.title)
    book.set_language(metadata.language)
    book.add_author(metadata.author)

    book.add_metadata("DC", "description", metadata.description)
    book.add_metadata("DC", "subject", ", ".join(metadata.keywords))

    epub_chapters = []
    for idx, (chapter_title, chapter_body) in enumerate(zip(chapter_titles, chapters), start=1):
        chapter = epub.EpubHtml(title=chapter_title, file_name=f"chap_{idx}.xhtml", lang=metadata.language)
        chapter.content = f"<h1>{chapter_title}</h1><p>{chapter_body.replace(chr(10), '</p><p>')}</p>"
        book.add_item(chapter)
        epub_chapters.append(chapter)

    book.toc = tuple(epub_chapters)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ["nav", *epub_chapters]

    epub.write_epub(str(output_path), book, {})
    return output_path
