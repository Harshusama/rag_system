from app.retriver import retrieve_chunks


question = input("Ask a question about your PDF: ")

results = retrieve_chunks(question)

print(f"\nRetrieved {len(results)} chunks")

for position, result in enumerate(results, start=1):
    print(f"\nResult {position}")
    print("ID:", result["id"])
    print("Source:", result["metadata"]["source"])
    print("Page:", result["metadata"]["page"])
    print("Chunk:", result["metadata"]["chunk"])
    print("Distance:", round(result["distance"], 4))
    print("Text:", result["text"][:500])