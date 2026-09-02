from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str

    chat_model: str = "gpt-4.1-mini"
    embedding_model: str = "text-embedding-3-small"

    chunk_size: int = 800
    chunk_overlap: int = 120
    retrieval_top_k: int = 5

    chroma_path: str = "chroma_db"
    collection_name: str = "production_rag"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()