import re
from pathlib import Path

import fitz


def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def load_pdf(file_path: str) -> list[dict]:
    pdf_path = Path(file_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {file_path}")

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF files are supported")

    pages = []

    with fitz.open(pdf_path) as document:
        for page_number, page in enumerate(document, start=1):
            raw_text = page.get_text("text")
            cleaned_text = clean_text(raw_text)

            if not cleaned_text:
                continue

            pages.append(
                {
                    "text": cleaned_text,
                    "metadata": {
                        "source": pdf_path.name,
                        "page": page_number,
                    },
                }
            )

    if not pages:
        raise ValueError(
            "No readable text was found in the PDF. "
            "The document may be empty or scanned."
        )

    return pages