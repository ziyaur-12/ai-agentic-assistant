print("Step 1: RAG test shuru")

from langchain_community.document_loaders import PyPDFLoader

print("Step 2: Loader import ho gaya")

# Apna PDF ka naam yaha daalo (jo tumne uploaded_docs me rakha hai)
pdf_path = "data/uploaded_docs/sample.pdf"

loader = PyPDFLoader(pdf_path)
documents = loader.load()

print(f"Step 3: PDF load ho gayi. Total pages: {len(documents)}")
print("\nPehle page ka content (first 300 characters):")
print(documents[0].page_content[:300])

from langchain.text_splitter import RecursiveCharacterTextSplitter

print("\nStep 4: Splitter import ho gaya")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)
chunks = splitter.split_documents(documents)

print(f"Step 5: Document ko {len(chunks)} chunks me tod diya gaya")
print("\nPehle chunk ka content:")
print(chunks[0].page_content[:300])
import re

def clean_pdf_text(text):
    # Single-letter spacing ko normal words mein convert karega:
    # "H a c k" -> "Hack"
    text = re.sub(r'(?<=\b[a-zA-Z])\s(?=[a-zA-Z]\b)', '', text)

    # Extra spaces/newlines normalize karega
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n\s*\n+', '\n\n', text)

    return text.strip()

cleaned_chunks = []

for chunk in chunks:
    chunk.page_content = clean_pdf_text(chunk.page_content)
    cleaned_chunks.append(chunk)

print("\nStep 6: Text clean ho gaya")
print("\nCleaned first chunk:")
print(cleaned_chunks[0].page_content[:500])
