
from pathlib import Path

from backend.config import (
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE_BYTES,
    MAX_FILENAME_LENGTH,
)


def validate_document(filename: str, file_size: int) -> tuple[bool, str]:
    if not filename or not filename.strip():
        return False, "Filename cannot be empty."

    if len(filename) > MAX_FILENAME_LENGTH:
        return False, "Filename is too long."

    if "\x00" in filename:
        return False, "Filename contains invalid characters."

    if "/" in filename or "\\" in filename:
        return False, "Filename must not contain a directory path."

    if filename in {".", ".."}:
        return False, "Invalid filename."

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        return False, f"File type not allowed: {extension or 'unknown'}"

    if file_size <= 0:
        return False, "Empty files are not allowed."

    if file_size > MAX_FILE_SIZE_BYTES:
        return False, "File exceeds the 5 MB size limit."

    return True, "Document passed ingestion policy."
