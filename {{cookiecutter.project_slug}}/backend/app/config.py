"""
Application configuration
"""
import os
from pydantic_settings import BaseSettings
from typing import Literal


class Config(BaseSettings):
    # Database
    database_url: str = os.environ.get("DATABASE_URL", "")
    
    # LLM Provider: ollama, openai, azure_openai
    llm_provider: Literal["ollama", "openai", "azure_openai"] = os.environ.get("LLM_PROVIDER", "{{ cookiecutter.llm_provider }}")
    
    # Ollama (local)
    ollama_base_url: str = os.environ.get("OLLAMA_BASE_URL", "http://ollama:11434")
    ollama_model: str = os.environ.get("OLLAMA_MODEL", "{{ cookiecutter.ollama_model }}")
    ollama_embedding_model: str = os.environ.get("OLLAMA_EMBEDDING_MODEL", "{{ cookiecutter.embedding_model }}")
    
    # OpenAI
    openai_api_key: str = os.environ.get("OPENAI_API_KEY", "")
    openai_model: str = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    openai_embedding_model: str = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    
    # Azure OpenAI
    azure_openai_api_key: str = os.environ.get("AZURE_OPENAI_API_KEY", "")
    azure_openai_endpoint: str = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
    azure_openai_api_version: str = os.environ.get("AZURE_OPENAI_API_VERSION", "2024-02-01")
    azure_openai_deployment: str = os.environ.get("AZURE_OPENAI_DEPLOYMENT", "")
    azure_openai_embedding_deployment: str = os.environ.get("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "")
    
    # MCP
    {% if cookiecutter.project_type == 'rag' %}
    mcp_search_url: str = os.environ.get("MCP_SEARCH_URL", "http://mcp-search:7071/mcp")
    {% endif %}

    {% if cookiecutter.project_type == 'chatbot' %}
    mcp_memory_url: str = os.environ.get("MCP_MEMORY_URL", "http://mcp-memory:7071/mcp")
    {% endif %}

    {% if cookiecutter.project_type in ['agent', 'multi_agent'] %}
    mcp_tools_url: str = os.environ.get("MCP_TOOLS_URL", "http://mcp-tools:7071/mcp")
    {% endif %}

    {% if cookiecutter.project_type == 'multi_agent' %}
    mcp_coordination_url: str = os.environ.get("MCP_COORDINATION_URL", "http://mcp-coordination:7073/mcp")
    {% endif %}
    {% if cookiecutter.use_auth == 'yes' %}
    # JWT
    jwt_secret_key: str = os.environ.get("JWT_SECRET_KEY", "{{ cookiecutter.jwt_secret }}")
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = int(os.environ.get("JWT_EXPIRE_MINUTES", "60"))
    {% endif %}
    



cfg = Config()
