from app.config import get_settings


settings = get_settings()


def split_text(
    text: str,
    chunk_size: int,
    chunk_overlap: int,
) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero")

    if chunk_overlap < 0:
        raise ValueError("Chunk overlap cannot be negative")

    if chunk_overlap >= chunk_size:
        raise ValueError("Chunk overlap must be smaller than chunk size")

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end]

        if end < text_length:
            last_break = max(
                chunk.rfind("\n\n"),
                chunk.rfind(". "),
                chunk.rfind(" "),
            )

            minimum_break = int(chunk_size * 0.6)

            if last_break >= minimum_break:
                end = start + last_break + 1
                chunk = text[start:end]

        chunk = chunk.strip()

        if chunk:
            chunks.append(chunk)

        if end >= text_length:
            break

        start = end - chunk_overlap

    return chunks


def create_chunks(pages: list[dict]) -> list[dict]:
    all_chunks = []

    for page in pages:
        page_chunks = split_text(
            text=page["text"],
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )

        for chunk_number, chunk_text in enumerate(
            page_chunks,
            start=1,
        ):
            chunk_id = (
                f'{page["metadata"]["source"]}'
                f'_page_{page["metadata"]["page"]}'
                f'_chunk_{chunk_number}'
            )

            all_chunks.append(
                {
                    "id": chunk_id,
                    "text": chunk_text,
                    "metadata": {
                        **page["metadata"],
                        "chunk": chunk_number,
                    },
                }
            )

    return all_chunks