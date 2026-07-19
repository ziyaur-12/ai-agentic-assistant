from langgraph.graph import StateGraph, END
from typing import TypedDict
from app.agents.rag_agent import run_rag_agent
from app.agents.researcher_agent import run_researcher_agent
from app.agents.writer_agent import run_writer_agent
from app.memory.conversation_memory import get_session_memory
from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY, LLM_MODEL

llm = ChatGroq(model=LLM_MODEL, temperature=0, api_key=GROQ_API_KEY)

class AgentState(TypedDict):
    query: str
    route: str
    raw_result: str
    final_answer: str
    session_id: str

def decide_route(state: AgentState):
    query = state["query"]
    decision_prompt = f"""User query: {query}

You must classify this query into exactly one category:
- "rag": if the query is about a person, resume, candidate, skills, certifications, projects, education, experience, or ANY topic that could be found in an uploaded document.
- "research": ONLY if the query explicitly asks for current events, latest news, today's date, live prices, or real-time information from the internet.

If you are unsure, always choose "rag".
Respond with exactly one word: rag or research"""
    result = llm.invoke(decision_prompt).content.strip().lower()
    print(f"   [Orchestrator decided: {result}]")
    return {"route": result}

def call_rag(state: AgentState):
    return {"raw_result": run_rag_agent(state["query"])}

def call_research(state: AgentState):
    return {"raw_result": run_researcher_agent(state["query"])}

def call_writer(state: AgentState):
    return {"final_answer": run_writer_agent(state["raw_result"])}

def router(state: AgentState):
    return "rag" if "rag" in state["route"] else "research"

graph = StateGraph(AgentState)
graph.add_node("decide", decide_route)
graph.add_node("rag", call_rag)
graph.add_node("research", call_research)
graph.add_node("writer", call_writer)

graph.set_entry_point("decide")
graph.add_conditional_edges("decide", router, {"rag": "rag", "research": "research"})
graph.add_edge("rag", "writer")
graph.add_edge("research", "writer")
graph.add_edge("writer", END)

app_graph = graph.compile()

def run_orchestrator(query: str, session_id: str = "default"):
    memory = get_session_memory(session_id)

    result = app_graph.invoke({"query": query, "session_id": session_id})
    answer = result["final_answer"]

    # Memory me save karo
    memory.add_message("user", query)
    memory.add_message("assistant", answer)

    return answer