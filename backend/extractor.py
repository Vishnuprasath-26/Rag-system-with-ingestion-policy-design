
from pathlib import Path

from docx import Document
from pypdf import PdfReader


def extract_text(file_path: str | Path) -> str:
    path = Path(file_path)
    extension = path.suffix.lower()

    if extension == ".txt":
        text = path.read_text(encoding="utf-8")

    elif extension == ".pdf":
        reader = PdfReader(str(path))
        text = "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

    elif extension == ".docx":
        document = Document(str(path))
        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

    else:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )

    text = text.strip()

    if not text:
        raise ValueError(
            "No readable text found in the document."
        )

    return text
