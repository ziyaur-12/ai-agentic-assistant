from langchain_groq import ChatGroq
from app.rag.vectorstore import retrieve_relevant_chunks
from app.prompts.system_prompts import RAG_AGENT_PROMPT
from app.config import GROQ_API_KEY, LLM_MODEL

llm = ChatGroq(model=LLM_MODEL, temperature=0, api_key=GROQ_API_KEY)

def run_rag_agent(question: str):
    chunks = retrieve_relevant_chunks(question, k=5)
    context = "\n\n".join([c.page_content for c in chunks])

    # Unique source filenames nikalo
    sources = list(set([c.metadata.get("source", "Unknown") for c in chunks]))

    prompt = RAG_AGENT_PROMPT.format(context=context, question=question)
    response = llm.invoke(prompt)

    answer = response.content
    if sources and sources != ["Unknown"]:
        source_list = ", ".join(sources)
        answer += f"\n\n---\n*Source(s): {source_list}*"

    return answer