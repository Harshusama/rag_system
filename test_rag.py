from app.rag_service import answer_question


question = input("Ask a question about your PDF: ")

result = answer_question(question)

print("\nQuestion:")
print(result["question"])

print("\nAnswer:")
print(result["answer"])

print("\nRetrieved chunks:")
print(result["retrieved_chunks"])

print("\nSources:")

for source in result["sources"]:
    print(
        f"- {source['source']}, "
        f"page {source['page']}"
    )