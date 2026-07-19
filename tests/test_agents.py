import pytest
from app.agents.rag_agent import run_rag_agent
from app.agents.writer_agent import run_writer_agent
from app.utils.helpers import is_valid_pdf, clean_text

def test_is_valid_pdf():
    assert is_valid_pdf("document.pdf") == True
    assert is_valid_pdf("document.txt") == False

def test_clean_text():
    dirty = "  Hello    World  \n\n  "
    assert clean_text(dirty) == "Hello World"

def test_writer_agent_returns_string():
    result = run_writer_agent("Raw test data yaha hai.")
    assert isinstance(result, str)
    assert len(result) > 0

# Note: RAG agent test ke liye vectorstore already populated hona chahiye
# Isliye ye test tabhi chalega jab tumne pehle koi document upload/index kiya ho
def test_rag_agent_returns_string():
    result = run_rag_agent("Test question")
    assert isinstance(result, str)