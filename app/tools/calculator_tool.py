from langchain.tools import tool

@tool
def calculator(expression: str) -> str:
    """Evaluates a simple math expression and returns the result."""
    try:
        return str(eval(expression, {"__builtins__": {}}, {}))
    except Exception:
        return "Invalid expression"