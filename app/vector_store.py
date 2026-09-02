import chromadb

from app.config import get_settings
from app.embedding_server import create_embeddings


settings = get_settings()

chroma_client = chromadb.PersistentClient(
    path=settings.chroma_path
)

collection = chroma_client.get_or_create_collection(
    name=settings.collection_name,
    metadata={"hnsw:space": "cosine"},
)


def store_chunks(
    chunks: list[dict],
    batch_size: int = 100,
) -> int:
    if not chunks:
        return 0

    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]

        ids = [chunk["id"] for chunk in batch]
        texts = [chunk["text"] for chunk in batch]
        metadatas = [chunk["metadata"] for chunk in batch]

        embeddings = create_embeddings(texts)

        collection.upsert(
            ids=ids,
            documents=texts,
            metadatas=metadatas,
            embeddings=embeddings,
        )

    return len(chunks)


def get_collection_count() -> int:
    return collection.count()