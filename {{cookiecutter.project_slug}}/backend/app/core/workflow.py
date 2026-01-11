"""
Agent workflow definition
"""
from langgraph.graph import StateGraph, END

# from app.core.state import RAGState, ChatState, AgentState, MultiAgentState

def get_graph():
    """Factory to get the appropriate graph based on project type"""
    
    {% if cookiecutter.project_type == 'rag' %}
    # from app.core.state import RAGState
    def build_rag_graph():
        """Build RAG workflow"""
        # graph = StateGraph(RAGState)
        # graph.add_node("rewrite", rewrite_query)
        # graph.add_node("retrieve", retrieve)
        # graph.add_node("grade", grade_relevance)
        # graph.add_node("generate", generate)
        # graph.set_entry_point("rewrite")
        # return graph.compile()
        pass
    return build_rag_graph()
    {% endif %}

    {% if cookiecutter.project_type == 'chatbot' %}
    # from app.core.state import ChatState
    def build_chat_graph():
        """Build Chat workflow"""
        # graph = StateGraph(ChatState)
        # graph.add_node("respond", generate_response)
        # graph.set_entry_point("respond")
        # return graph.compile()
        pass
    return build_chat_graph()
    {% endif %}

    {% if cookiecutter.project_type == 'agent' %}
    # from app.core.state import AgentState
    def build_agent_graph():
        """Build Agent workflow"""
        # graph = StateGraph(AgentState)
        # graph.add_node("plan", plan_action)
        # graph.add_node("act", call_tool)
        # graph.add_node("observe", process_result)
        # graph.add_node("respond", generate_response)
        # graph.set_entry_point("plan")
        # graph.add_conditional_edges("observe", should_continue, {"continue": "plan", "end": "respond"})
        # return graph.compile()
        pass
    return build_agent_graph()
    {% endif %}

    {% if cookiecutter.project_type == 'multi_agent' %}
    # from app.core.state import MultiAgentState
    def build_multi_agent_graph():
        """Build Multi-Agent workflow"""
        # graph = StateGraph(MultiAgentState)
        # graph.add_node("supervisor", route_to_agent)
        # graph.add_node("researcher", researcher_agent)
        # graph.add_node("writer", writer_agent)
        # graph.add_node("critic", critic_agent)
        # graph.add_node("synthesize", combine_results)
        # graph.set_entry_point("supervisor")
        # return graph.compile()
        pass
    return build_multi_agent_graph()
    {% endif %}
