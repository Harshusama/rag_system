from pydantic import BaseModel, Field


class QuestionRequest(BaseModel):
    question: str = Field(
        min_length=2,
        max_length=2000,
    )

    top_k: int | None = Field(
        default=None,
        ge=1,
        le=20,
    )


class SourceResponse(BaseModel):
    source: str
    page: int


class QuestionResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceResponse]
    retrieved_chunks: int


class UploadResponse(BaseModel):
    filename: str
    readable_pages: int
    chunks_created: int
    total_chunks: int
    message: str