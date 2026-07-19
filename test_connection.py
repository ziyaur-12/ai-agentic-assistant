print("Step 1: Script shuru ho gayi")

from dotenv import load_dotenv
import os

print("Step 2: Imports ho gaye")

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
print("Step 3: API key mili:", api_key)

from langchain_groq import ChatGroq
print("Step 4: LangChain Groq import ho gaya")

llm = ChatGroq(model="openai/gpt-oss-120b", api_key=api_key)
print("Step 5: LLM object bana")

response = llm.invoke("Hello")
print("Step 6: Response mila:")
print(response.content)