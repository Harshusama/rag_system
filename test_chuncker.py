from app.chuncker import create_chunks
from app.loader import load_pdf


pages = load_pdf("data/Case Study Harshitha.pdf")
chunks = create_chunks(pages)

print("Number of pages:", len(pages))
print("Number of chunks:", len(chunks))

for chunk in chunks[:3]:
    print("\nID:", chunk["id"])
    print("Metadata:", chunk["metadata"])
    print("Length:", len(chunk["text"]))
    print("Text:", chunk["text"][:300])