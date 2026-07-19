print("Step 1: Web search test shuru")

from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv
import os

load_dotenv()
tavily_key = os.getenv("TAVILY_API_KEY")
print("Step 2: Tavily key mili:", tavily_key[:10] + "...")

os.environ["TAVILY_API_KEY"] = tavily_key

search_tool = TavilySearchResults(max_results=3)
print("Step 3: Search tool ready")

query = "latest AI news today"
print(f"Step 4: Search kar rahe hain: '{query}'")

results = search_tool.invoke(query)

print("\n=== SEARCH RESULTS ===")
for i, result in enumerate(results):
    print(f"\n--- Result {i+1} ---")
    print("URL:", result.get("url", "N/A"))
    print("Content:", result.get("content", "N/A")[:200])