"""License document generation for publishing outputs."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from config import LICENSE_FILE_NAME, OUTPUT_DIR



def generate_publishing_license(title: str, author: str, isbn: str, output_dir: Path = OUTPUT_DIR) -> Path:
    """Create a simple publishing license text file for the generated book."""
    output_dir.mkdir(parents=True, exist_ok=True)
    content = f"""ABITALIB Publishing License
=========================
Date: {datetime.utcnow().isoformat()} UTC

Book Title: {title}
Author: {author}
ISBN: {isbn}

License Terms:
1. This document certifies the generated work as an AI-assisted draft.
2. The owner is responsible for review, editing, legal compliance, and publication.
3. Redistribution of this license is allowed with attribution.
"""
    path = output_dir / LICENSE_FILE_NAME
    path.write_text(content, encoding="utf-8")
    return path
