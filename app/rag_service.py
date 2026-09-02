from openai import OpenAI

from app.config import get_settings
from app.retriver import retrieve_chunks


settings = get_settings()

client = OpenAI(api_key=settings.openai_api_key)


SYSTEM_PROMPT = """
You are a document-question-answering assistant.

Answer the user's question using only the provided document context.

Rules:
1. Do not use outside knowledge.
2. If the context does not contain the answer, say:
   "I could not find that information in the provided documents."
3. Do not invent facts, names, dates or numbers.
4. Cite supporting information using this format:
   [Source: filename, page X]
5. Keep the answer clear and concise.
""".strip()


def build_context(chunks: list[dict]) -> str:
    context_sections = []

    for position, chunk in enumerate(chunks, start=1):
        metadata = chunk["metadata"]

        section = (
            f"Context {position}\n"
            f"Source: {metadata['source']}\n"
            f"Page: {metadata['page']}\n"
            f"Content:\n{chunk['text']}"
        )

        context_sections.append(section)

    return "\n\n---\n\n".join(context_sections)


def build_sources(chunks: list[dict]) -> list[dict]:
    sources = []
    seen_sources = set()

    for chunk in chunks:
        metadata = chunk["metadata"]

        source_key = (
            metadata["source"],
            metadata["page"],
        )

        if source_key in seen_sources:
            continue

        seen_sources.add(source_key)

        sources.append(
            {
                "source": metadata["source"],
                "page": metadata["page"],
            }
        )

    return sources


def answer_question(question: str) -> dict:
    relevant_chunks = retrieve_chunks(question)

    context = build_context(relevant_chunks)

    user_prompt = f"""
Document context:

{context}

User question:

{question}
""".strip()

    response = client.responses.create(
        model=settings.chat_model,
        instructions=SYSTEM_PROMPT,
        input=user_prompt,
    )

    answer = response.output_text.strip()

    return {
        "question": question,
        "answer": answer,
        "sources": build_sources(relevant_chunks),
        "retrieved_chunks": len(relevant_chunks),
    }