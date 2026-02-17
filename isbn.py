"""ISBN and barcode generation utilities."""

from __future__ import annotations

import random
from pathlib import Path

import barcode
from barcode.writer import ImageWriter

from config import ISBN_OUTPUT_NAME, OUTPUT_DIR



def _isbn13_check_digit(twelve_digits: str) -> str:
    """Compute ISBN-13 check digit from first 12 digits."""
    total = 0
    for idx, value in enumerate(twelve_digits):
        number = int(value)
        total += number if idx % 2 == 0 else number * 3
    check = (10 - (total % 10)) % 10
    return str(check)



def generate_sample_isbn() -> str:
    """Create a pseudo-random ISBN-13 string for sample publishing output."""
    prefix = "978"
    body = "".join(str(random.randint(0, 9)) for _ in range(9))
    first_twelve = prefix + body
    return first_twelve + _isbn13_check_digit(first_twelve)



def create_isbn_barcode(isbn_value: str, output_dir: Path = OUTPUT_DIR) -> Path:
    """Generate and save a barcode PNG image for a given ISBN value."""
    output_dir.mkdir(parents=True, exist_ok=True)
    isbn_class = barcode.get_barcode_class("isbn13")
    barcode_obj = isbn_class(isbn_value, writer=ImageWriter())
    file_path = barcode_obj.save(str(output_dir / ISBN_OUTPUT_NAME))
    return Path(file_path)
