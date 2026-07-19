print("Step 1: Researcher agent test shuru")

from langchain.agents import create_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")
tavily_key = os.getenv("TAVILY_API_KEY")
os.environ["TAVILY_API_KEY"] = tavily_key

print("Step 2: Keys load ho gayi")

llm = ChatGroq(model="openai/gpt-oss-120b", api_key=groq_key)
search_tool = TavilySearchResults(max_results=2)
tools = [search_tool]

print("Step 3: LLM aur tools ready")

# --- YE NAYA PART HAI: Language Control ---
LANGUAGE_PREFERENCE = "english"   # "english" ya "hindi" daal do jo chahiye

language_instruction = {
    "english": "You must respond ONLY in English, using Roman script. Even if the user's question is written in Hindi or Hinglish, your entire answer must be in English. Do not use Devanagari script under any circumstances.",

    "hindi": "You must respond ONLY in Hindi using Devanagari script (जैसे यह वाक्य). Do not use English, regardless of the language of the question.",
}

system_prompt = f"""You are a research assistant. If current or latest information is needed, use the web_search tool.
{language_instruction[LANGUAGE_PREFERENCE]}
"""
# --- YAHAN TAK ---

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt
)

print("Step 4: Agent ready hai, ab query bhej rahe hain...")

query = "Groq company ke baare me batao aur ye batao ki unka latest model kaunsa hai"

result = agent.invoke({
    "messages": [{"role": "user", "content": query}]
})

print("\n=== FINAL ANSWER ===")
print(result["messages"][-1].content)