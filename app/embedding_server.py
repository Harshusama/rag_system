from openai import OpenAI

from app.config import get_settings


settings = get_settings()

client = OpenAI(api_key=settings.openai_api_key)


def create_embeddings(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    response = client.embeddings.create(
        model=settings.embedding_model,
        input=texts,
    )

    embeddings = [
        item.embedding
        for item in response.data
    ]

    return embeddings