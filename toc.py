"""Automatic table-of-contents helper functions."""

from typing import List



def create_toc(chapter_titles: List[str]) -> str:
    """Create a plain-text table of contents from chapter titles."""
    lines = ["Table of Contents", "================="]
    for index, title in enumerate(chapter_titles, start=1):
        lines.append(f"{index}. {title}")
    return "\n".join(lines)
