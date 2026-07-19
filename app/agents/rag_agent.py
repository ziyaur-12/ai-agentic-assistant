from langchain_groq import ChatGroq
from app.rag.vectorstore import retrieve_relevant_chunks
from app.prompts.system_prompts import RAG_AGENT_PROMPT
from app.config import GROQ_API_KEY, LLM_MODEL

llm = ChatGroq(model=LLM_MODEL, temperature=0, api_key=GROQ_API_KEY)

def run_rag_agent(question: str):
    chunks = retrieve_relevant_chunks(question)
    context = "\n\n".join([c.page_content for c in chunks])
    prompt = RAG_AGENT_PROMPT.format(context=context, question=question)
    response = llm.invoke(prompt)
    return response.content