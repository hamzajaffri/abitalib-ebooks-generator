"""Chapter memory and summary management for coherent multi-chapter generation."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from config import MEMORY_DIR


@dataclass
class ChapterMemory:
    """Tracks chapter content and per-chapter summaries."""

    title: str
    summaries: List[str] = field(default_factory=list)
    chapters: List[str] = field(default_factory=list)

    def add_chapter(self, chapter_text: str, summary: str) -> None:
        """Append chapter content and summary to memory."""
        self.chapters.append(chapter_text)
        self.summaries.append(summary)

    def rolling_context(self, window: int = 3) -> str:
        """Build compact context from the latest chapter summaries."""
        selected = self.summaries[-window:] if self.summaries else []
        if not selected:
            return "No previous chapters yet."
        return "\n".join(f"- {item}" for item in selected)

    def save(self) -> Path:
        """Persist memory state as JSON in the local memory directory."""
        MEMORY_DIR.mkdir(parents=True, exist_ok=True)
        safe_name = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in self.title.lower())
        path = MEMORY_DIR / f"{safe_name}.json"
        payload = {"title": self.title, "summaries": self.summaries, "chapters": self.chapters}
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        return path
