from fastapi import FastAPI, UploadFile
from app.schemas.models import QueryRequest, QueryResponse
from app.agents.orchestrator import run_orchestrator
from app.rag.loader import load_document
from app.rag.splitter import split_documents
from app.rag.vectorstore import create_vectorstore
from app.memory.conversation_memory import get_session_memory, list_all_sessions
from app.auth.users import signup, login
import shutil
import os

os.makedirs("data/uploaded_docs", exist_ok=True)
os.makedirs("vectordb", exist_ok=True)

app = FastAPI()

@app.post("/upload")
async def upload_doc(file: UploadFile):
    allowed_extensions = [".pdf", ".docx", ".txt"]
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in allowed_extensions:
        return {"status": "error", "message": f"Unsupported file type: {ext}. Allowed: PDF, DOCX, TXT"}

    path = f"data/uploaded_docs/{file.filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    docs = load_document(path)
    chunks = split_documents(docs)
    create_vectorstore(chunks, source_name=file.filename)
    return {"status": "uploaded and indexed", "filename": file.filename}

@app.post("/query", response_model=QueryResponse)
async def query_agent(request: QueryRequest):
    session_id = request.session_id if request.session_id else "default"
    answer = run_orchestrator(request.query, session_id)
    return QueryResponse(answer=answer)

@app.get("/history/{session_id}")
async def get_history(session_id: str):
    memory = get_session_memory(session_id)
    return {"history": memory.get_history()}

@app.delete("/history/{session_id}")
async def clear_history(session_id: str):
    memory = get_session_memory(session_id)
    memory.clear()
    return {"status": "history cleared"}

@app.get("/sessions")
async def get_all_sessions():
    return {"sessions": list_all_sessions()}
from pydantic import BaseModel

class AuthRequest(BaseModel):
    username: str
    password: str

@app.post("/signup")
async def signup_route(request: AuthRequest):
    return signup(request.username, request.password)

@app.post("/login")
async def login_route(request: AuthRequest):
    return login(request.username, request.password)