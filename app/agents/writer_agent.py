from langchain_groq import ChatGroq
from app.prompts.system_prompts import WRITER_PROMPT
from app.config import GROQ_API_KEY, LLM_MODEL

llm = ChatGroq(model=LLM_MODEL, temperature=0.3, api_key=GROQ_API_KEY)

def run_writer_agent(raw_data: str):
    prompt = f"{WRITER_PROMPT}\n\nRaw Data:\n{raw_data}"
    response = llm.invoke(prompt)
    return response.content