print("Step 1: Full RAG test shuru")

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

print("Step 2: Imports ho gaye")

# Vector store already bani hui hai (pehle test se), sidha load karte hain
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(persist_directory="vectordb/", embedding_function=embeddings)

print("Step 3: Vector store load ho gaya")

# User ka sawaal
question = "Is candidate ne kaunse hackathons participate kiye hain?"

# Relevant chunks dhoondo
results = db.similarity_search(question, k=3)
context = "\n\n".join([r.page_content for r in results])

print("Step 4: Relevant chunks mil gaye")

# LLM ko context + question do
llm = ChatGroq(model="openai/gpt-oss-120b", api_key=api_key)

prompt = f"""
Tum ek helpful assistant ho. Diye gaye context ka use karke user ke question ka answer do.
Agar context me answer nahi hai to bolo "Mujhe is document me ye jaankari nahi mili."

Context:
{context}

Question: {question}

Answer:
"""

print("Step 5: LLM ko bhej rahe hain...")
response = llm.invoke(prompt)

print("\n=== FINAL ANSWER ===")
print(response.content)