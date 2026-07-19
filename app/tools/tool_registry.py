from app.tools.web_search_tool import get_web_search_tool
from app.tools.calculator_tool import calculator

def get_all_tools():
    """Sab available tools ki list return karta hai — future me naye tools yaha add karo"""
    return [
        get_web_search_tool(),
        calculator
    ]

def get_tool_by_name(name: str):
    """Naam se specific tool dhoondhne ke liye"""
    tools = get_all_tools()
    for tool in tools:
        if tool.name == name:
            return tool
    return None