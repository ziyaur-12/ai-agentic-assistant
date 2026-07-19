print("Step 1: Vectorstore test shuru")

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

print("Step 2: Sab imports ho gaye")

# PDF load karo
pdf_path = "data/uploaded_docs/sample.pdf"
loader = PyPDFLoader(pdf_path)
documents = loader.load()
print(f"Step 3: PDF load ho gayi, {len(documents)} pages")

# Chunks me todo
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
chunks = splitter.split_documents(documents)
print(f"Step 4: {len(chunks)} chunks bane")

# Embedding model load karo (ye pehli baar thoda time lega, model download hoga)
print("Step 5: Embedding model load ho raha hai... (thoda time lagega pehli baar)")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
print("Step 6: Embedding model ready hai")

# Vector store banao
print("Step 7: Vector store bana rahe hain...")
db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="vectordb/"
)
print("Step 8: Vector store ban gaya aur save ho gaya!")

# Ab ek test query karte hain
print("\nStep 9: Test search kar rahe hain...")
query = "hackathon"
results = db.similarity_search(query, k=2)

print(f"\nQuery: '{query}' ke liye top 2 results:\n")
for i, result in enumerate(results):
    print(f"--- Result {i+1} ---")
    print(result.page_content[:200])
    print()