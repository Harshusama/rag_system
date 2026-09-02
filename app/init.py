from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile

from app.chuncker import create_chunks
from app.loader import load_pdf
from app.rag_service import answer_question
from app.schemas import (
    QuestionRequest,
    QuestionResponse,
    UploadResponse,
)
from app.vector_store import (
    get_collection_count,
    store_chunks,
)


app = FastAPI(
    title="Production RAG API",
    description=(
        "Upload PDF documents and ask questions "
        "using retrieval-augmented generation."
    ),
    version="1.0.0",
)

DATA_DIRECTORY = Path("data")
DATA_DIRECTORY.mkdir(exist_ok=True)

@app.get("/")
def home():
    return {
        "message": "Production RAG API is running"
    }


@app.get("/health")
def health_check() -> dict:
    return {
        "status": "healthy",
        "service": "production-rag-api",
    }


@app.get("/documents/count")
def document_count() -> dict:
    return {
        "stored_chunks": get_collection_count(),
    }


@app.post(
    "/upload",
    response_model=UploadResponse,
)
async def upload_pdf(
    file: UploadFile = File(...),
) -> UploadResponse:
    original_filename = Path(file.filename or "").name

    if not original_filename:
        raise HTTPException(
            status_code=400,
            detail="A filename is required.",
        )

    if Path(original_filename).suffix.lower() != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    unique_filename = (
        f"{uuid4().hex}_{original_filename}"
    )

    saved_path = DATA_DIRECTORY / unique_filename

    try:
        file_content = await file.read()

        if not file_content:
            raise HTTPException(
                status_code=400,
                detail="The uploaded PDF is empty.",
            )

        saved_path.write_bytes(file_content)

        pages = load_pdf(str(saved_path))
        chunks = create_chunks(pages)
        stored_count = store_chunks(chunks)

        return UploadResponse(
            filename=original_filename,
            readable_pages=len(pages),
            chunks_created=stored_count,
            total_chunks=get_collection_count(),
            message="PDF uploaded and ingested successfully.",
        )

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"PDF ingestion failed: {error}",
        ) from error

    finally:
        await file.close()


@app.post(
    "/ask",
    response_model=QuestionResponse,
)
def ask_question(
    request: QuestionRequest,
) -> QuestionResponse:
    try:
        result = answer_question(
            question=request.question,
            top_k=request.top_k,
        )

        return QuestionResponse(**result)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Question answering failed: {error}",
        ) from error