print("Step 1: Orchestrator test shuru")

from langgraph.graph import StateGraph, END
from typing import TypedDict
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import create_agent
from dotenv import load_dotenv
import os

load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
tavily_key = os.getenv("TAVILY_API_KEY")
os.environ["TAVILY_API_KEY"] = tavily_key

print("Step 2: Keys load ho gayi")

# Common LLM
llm = ChatGroq(model="openai/gpt-oss-120b", api_key=groq_key)

# --- RAG Setup ---
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = Chroma(persist_directory="vectordb/", embedding_function=embeddings)

def run_rag(question: str) -> str:
    results = db.similarity_search(question, k=3)
    context = "\n\n".join([r.page_content for r in results])
    prompt = f"""Answer the question using only the context below. If the answer isn't in the context, say so.

Context:
{context}

Question: {question}

Answer in English:"""
    response = llm.invoke(prompt)
    return response.content

# --- Researcher Setup ---
search_tool = TavilySearchResults(max_results=2)
researcher_agent = create_agent(
    model=llm,
    tools=[search_tool],
    system_prompt="You are a research assistant. Use web_search for current information. Always respond in clear English."
)

def run_researcher(question: str) -> str:
    result = researcher_agent.invoke({"messages": [{"role": "user", "content": question}]})
    return result["messages"][-1].content

print("Step 3: RAG aur Researcher functions ready")

# --- LangGraph State ---
class AgentState(TypedDict):
    query: str
    route: str
    final_answer: str

def decide_route(state: AgentState):
    query = state["query"]
    decision_prompt = f"""Query: {query}
If this is about an uploaded document/resume/personal file, respond only with: rag
If this needs current/latest/live internet information, respond only with: research
Answer with just one word: rag or research"""
    result = llm.invoke(decision_prompt).content.strip().lower()
    print(f"   [Orchestrator decided: {result}]")
    return {"route": result}

def call_rag(state: AgentState):
    return {"final_answer": run_rag(state["query"])}

def call_research(state: AgentState):
    return {"final_answer": run_researcher(state["query"])}

def router(state: AgentState):
    return "rag" if "rag" in state["route"] else "research"

graph = StateGraph(AgentState)
graph.add_node("decide", decide_route)
graph.add_node("rag", call_rag)
graph.add_node("research", call_research)

graph.set_entry_point("decide")
graph.add_conditional_edges("decide", router, {"rag": "rag", "research": "research"})
graph.add_edge("rag", END)
graph.add_edge("research", END)

app_graph = graph.compile()

print("Step 4: Graph compile ho gaya\n")

# --- Test 1: Document-based query ---
print("=== TEST 1: Document Query ===")
result1 = app_graph.invoke({"query": "Is candidate ne kaunse hackathons kiye hain?"})
print("Answer:", result1["final_answer"])

print("\n" + "="*50 + "\n")

# --- Test 2: Live info query ---
print("=== TEST 2: Live Info Query ===")
result2 = app_graph.invoke({"query": "What is Groq's latest AI model?"})
print("Answer:", result2["final_answer"])