from app.loader import load_pdf


pages = load_pdf("data/Case Study Harshitha.pdf")

print("PDF loaded successfully")
print("Number of readable pages:", len(pages))

for page in pages[:2]:
    print("\nMetadata:", page["metadata"])
    print("Text preview:", page["text"][:300])