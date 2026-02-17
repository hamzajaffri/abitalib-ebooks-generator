"""Core chapter generation engine that orchestrates prompts, memory, and summaries."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

from config import DEFAULT_MAX_TOKENS, DEFAULT_TEMPERATURE, DEFAULT_TOP_P
from memory_system import ChapterMemory
from model_loader import LocalModelLoader


@dataclass
class BookRequest:
    """Input parameters for book generation."""

    title: str
    author: str
    genre: str
    language: str
    chapter_count: int


class BookEngine:
    """Generate multi-chapter content with persistent rolling memory."""

    def __init__(self, model_loader: Optional[LocalModelLoader] = None) -> None:
        """Initialize engine with optional external model loader."""
        self.model_loader = model_loader or LocalModelLoader()

    def _chapter_prompt(self, request: BookRequest, chapter_number: int, memory: ChapterMemory) -> str:
        """Build a structured generation prompt for the model."""
        return f"""
You are a professional novelist.
Write Chapter {chapter_number} of a {request.genre} book in {request.language}.
Book title: {request.title}
Author: {request.author}

Story memory from previous chapters:
{memory.rolling_context(window=3)}

Instructions:
- Maintain continuity with previous chapters.
- Use vivid scene writing and dialogue where appropriate.
- End with a hook for the next chapter.
- Keep chapter length around 700-1000 words.
""".strip()

    def _summarize(self, chapter_text: str) -> str:
        """Create a compact summary from chapter text using model or fallback."""
        if self.model_loader.is_loaded:
            prompt = (
                "Summarize the following chapter in 4 concise bullet points for memory continuity:\n\n"
                f"{chapter_text}"
            )
            return self.model_loader.generate(prompt, max_tokens=220, temperature=0.3, top_p=0.95)

        lines = [line.strip() for line in chapter_text.split(".") if line.strip()]
        condensed = lines[:4] if lines else ["Chapter generated."]
        return "\n".join(f"- {line}." for line in condensed)

    def generate_book(self, request: BookRequest) -> Tuple[List[str], List[str], ChapterMemory]:
        """Generate chapter titles and content while updating memory summaries."""
        memory = ChapterMemory(title=request.title)
        chapter_titles: List[str] = []
        chapters: List[str] = []

        for chapter_number in range(1, request.chapter_count + 1):
            chapter_title = f"Chapter {chapter_number}: {request.genre.title()} Arc {chapter_number}"
            chapter_titles.append(chapter_title)

            if self.model_loader.is_loaded:
                chapter_prompt = self._chapter_prompt(request, chapter_number, memory)
                chapter_body = self.model_loader.generate(
                    chapter_prompt,
                    max_tokens=DEFAULT_MAX_TOKENS,
                    temperature=DEFAULT_TEMPERATURE,
                    top_p=DEFAULT_TOP_P,
                )
            else:
                chapter_body = (
                    f"{chapter_title}\n\n"
                    f"This is an offline fallback chapter for '{request.title}'. "
                    "Load a GGUF model for richer story quality. "
                    f"The protagonist evolves through a {request.genre} journey with thematic continuity."
                )

            summary = self._summarize(chapter_body)
            memory.add_chapter(chapter_body, summary)
            chapters.append(chapter_body)

        memory.save()
        return chapter_titles, chapters, memory
