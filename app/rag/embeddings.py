from langchain_huggingface import HuggingFaceEndpointEmbeddings
from app.config import EMBEDDING_MODEL, HUGGINGFACE_API_KEY

def get_embedding_model():
    return HuggingFaceEndpointEmbeddings(
        model=EMBEDDING_MODEL,
        huggingfacehub_api_token=HUGGINGFACE_API_KEY
    )