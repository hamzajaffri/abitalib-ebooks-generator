"""Local GGUF model loading utilities backed by llama.cpp bindings."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from config import DEFAULT_CTX_SIZE, DEFAULT_MODEL_PATH
from hardware import detect_hardware

try:
    from llama_cpp import Llama
except Exception:  # pragma: no cover - import failures are handled at runtime.
    Llama = None


@dataclass
class ModelConfig:
    """Model loading configuration values."""

    model_path: Path = DEFAULT_MODEL_PATH
    context_size: int = DEFAULT_CTX_SIZE
    verbose: bool = False


class LocalModelLoader:
    """Manages loading and inference with a local llama.cpp GGUF model."""

    def __init__(self, config: Optional[ModelConfig] = None) -> None:
        """Initialize loader with model config."""
        self.config = config or ModelConfig()
        self._model = None

    def _gpu_layers_for_hardware(self) -> int:
        """Estimate offloaded layers based on detected GPU memory."""
        hw = detect_hardware()
        if not hw.has_gpu:
            return 0
        if hw.gpu_vram_gb >= 20:
            return 50
        if hw.gpu_vram_gb >= 12:
            return 35
        if hw.gpu_vram_gb >= 8:
            return 20
        return 10

    def load_model(self, model_path: Optional[str] = None) -> None:
        """Load a GGUF model from disk into memory."""
        if Llama is None:
            raise RuntimeError(
                "llama-cpp-python is not installed or unavailable. Install requirements first."
            )

        path = Path(model_path or self.config.model_path).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(f"Model file not found: {path}")

        n_gpu_layers = self._gpu_layers_for_hardware()
        self._model = Llama(
            model_path=str(path),
            n_ctx=self.config.context_size,
            n_gpu_layers=n_gpu_layers,
            verbose=self.config.verbose,
        )

    @property
    def is_loaded(self) -> bool:
        """Return whether a model instance is currently loaded."""
        return self._model is not None

    def generate(self, prompt: str, max_tokens: int = 700, temperature: float = 0.7, top_p: float = 0.9) -> str:
        """Generate text from the loaded model for a given prompt."""
        if not self._model:
            raise RuntimeError("Model is not loaded. Call load_model() first.")

        response = self._model(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stop=["<|eot_id|>", "\nChapter"],
        )
        return response["choices"][0]["text"].strip()
