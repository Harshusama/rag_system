from app.config import get_settings
from app.embedding_server import create_embeddings
from app.vector_store import collection


settings = get_settings()


def retrieve_chunks(
    question: str,
    top_k: int | None = None,
) -> list[dict]:
    question = question.strip()

    if not question:
        raise ValueError("Question cannot be empty")

    collection_count = collection.count()

    if collection_count == 0:
        raise ValueError(
            "The vector database is empty. "
            "Ingest a PDF before asking questions."
        )

    number_of_results = top_k or settings.retrieval_top_k
    number_of_results = min(
        number_of_results,
        collection_count,
    )

    question_embedding = create_embeddings([question])[0]

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=number_of_results,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )

    retrieved_chunks = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]
    ids = results["ids"][0]

    for chunk_id, document, metadata, distance in zip(
        ids,
        documents,
        metadatas,
        distances,
    ):
        retrieved_chunks.append(
            {
                "id": chunk_id,
                "text": document,
                "metadata": metadata,
                "distance": distance,
            }
        )

    return retrieved_chunks