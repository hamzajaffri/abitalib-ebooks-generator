"""Global configuration for ABITALIB E-Books Generator."""

from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
MODEL_DIR = BASE_DIR / "models"
MEMORY_DIR = BASE_DIR / "memory"

# Application defaults
DEFAULT_MODEL_PATH = MODEL_DIR / "model.gguf"
DEFAULT_CTX_SIZE = 4096
DEFAULT_MAX_TOKENS = 900
DEFAULT_TEMPERATURE = 0.7
DEFAULT_TOP_P = 0.9
DEFAULT_CHAPTER_COUNT = 6

# Generation safety caps
MIN_CHAPTERS = 1
MAX_CHAPTERS = 30
MAX_TITLE_LENGTH = 150
MAX_AUTHOR_LENGTH = 120

# File generation
PDF_FONT_NAME = "Times-Roman"
PDF_TITLE_FONT_SIZE = 20
PDF_BODY_FONT_SIZE = 12
ISBN_OUTPUT_NAME = "isbn_barcode"
LICENSE_FILE_NAME = "publishing_license.txt"


def ensure_directories() -> None:
    """Create required working directories if they do not exist."""
    for directory in (OUTPUT_DIR, MODEL_DIR, MEMORY_DIR):
        directory.mkdir(parents=True, exist_ok=True)


ensure_directories()
