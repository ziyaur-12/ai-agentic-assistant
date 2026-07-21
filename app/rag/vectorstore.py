from langchain_community.vectorstores import Chroma
from app.rag.embeddings import get_embedding_model
from app.config import VECTOR_DB_PATH

def create_vectorstore(chunks, source_name=None):
    """Chunks ko vectorstore me add karta hai. Agar already store exist karta hai, usme add hota hai (overwrite nahi)."""
    embeddings = get_embedding_model()

    # Har chunk me source filename tag karo (agar diya gaya hai)
    if source_name:
        for chunk in chunks:
            chunk.metadata["source"] = source_name

    db = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )
    db.add_documents(chunks)
    return db

def load_vectorstore():
    embeddings = get_embedding_model()
    return Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )

def retrieve_relevant_chunks(query, k=5):
    db = load_vectorstore()
    return db.similarity_search(query, k=k)