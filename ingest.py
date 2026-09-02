from app.chuncker import create_chunks
from app.loader import load_pdf
from app.vector_store import (
    get_collection_count,
    store_chunks,
)


def ingest_pdf(file_path: str) -> None:
    print("Loading PDF...")
    pages = load_pdf(file_path)

    print(f"Readable pages: {len(pages)}")

    print("Creating chunks...")
    chunks = create_chunks(pages)

    print(f"Chunks created: {len(chunks)}")

    print("Generating embeddings and storing chunks...")
    stored_count = store_chunks(chunks)

    print(f"Chunks processed: {stored_count}")
    print(f"Total chunks in ChromaDB: {get_collection_count()}")


if __name__ == "__main__":
    ingest_pdf("data/Case Study Harshitha.pdf")