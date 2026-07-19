from langchain.agents import create_agent
from langchain_groq import ChatGroq
from app.tools.web_search_tool import get_web_search_tool
from app.prompts.system_prompts import RESEARCHER_PROMPT
from app.config import GROQ_API_KEY, LLM_MODEL

llm = ChatGroq(model=LLM_MODEL, temperature=0, api_key=GROQ_API_KEY)
tools = [get_web_search_tool()]

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=RESEARCHER_PROMPT
)

def run_researcher_agent(query: str):
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content