"""Metadata generation utilities for title variants, keywords, and descriptions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class BookMetadata:
    """Simple metadata container for e-book exports."""

    title: str
    subtitle: str
    author: str
    language: str
    keywords: List[str]
    description: str



def generate_metadata(title: str, author: str, genre: str, language: str) -> BookMetadata:
    """Generate book metadata fields from user inputs."""
    keywords = [
        genre,
        f"{genre} novel",
        "AI generated book",
        title,
        author,
    ]
    subtitle = f"An AI-crafted {genre} story"
    description = (
        f"{title} is an original {genre} work by {author}, generated with the "
        "ABITALIB E-Books Generator local AI workflow."
    )
    return BookMetadata(
        title=title,
        subtitle=subtitle,
        author=author,
        language=language,
        keywords=keywords,
        description=description,
    )
