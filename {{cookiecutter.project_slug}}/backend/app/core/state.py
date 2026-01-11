"""
Agent state definitions
"""
from typing import TypedDict, Annotated, List, Union
from langgraph.graph.message import add_messages


{% if cookiecutter.project_type == 'rag' %}
class RAGState(TypedDict):
    question: str
    rewritten_query: str
    chunks: List[dict]
    answer: str
    citations: List[dict]
{% endif %}

{% if cookiecutter.project_type == 'chatbot' %}
class ChatState(TypedDict):
    messages: List[dict]
    response: str
{% endif %}

{% if cookiecutter.project_type == 'agent' %}
class AgentState(TypedDict):
    messages: Annotated[List[dict], add_messages]
    tool_calls: List[dict]
    tool_results: List[dict]
    final_answer: str
{% endif %}

{% if cookiecutter.project_type == 'multi_agent' %}
class MultiAgentState(TypedDict):
    task: str
    agents: List[str]
    messages: List[dict]
    current_agent: str
    results: dict
    final_output: str
{% endif %}
