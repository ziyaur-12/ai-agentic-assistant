from langchain_community.vectorstores import Chroma
from app.rag.embeddings import get_embedding_model
from app.config import VECTOR_DB_PATH

def create_vectorstore(chunks):
    embeddings = get_embedding_model()
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH
    )
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