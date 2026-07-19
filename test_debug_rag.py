from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(persist_directory="vectordb/", embedding_function=embeddings)

# Check kitne documents hain vectorstore me
results = db.similarity_search("technical skills", k=5)
print(f"Total chunks mile: {len(results)}\n")

for i, r in enumerate(results):
    print(f"--- Chunk {i+1} ---")
    print(r.page_content[:300])
    print()