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
    mcp_search_url: str = os.environ.get("MCP_SEARCH_URL", "http://mcp-search:7071/mcp")
    {% if cookiecutter.use_auth == 'yes' %}
    # JWT
    jwt_secret_key: str = os.environ.get("JWT_SECRET_KEY", "{{ cookiecutter.jwt_secret }}")
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = int(os.environ.get("JWT_EXPIRE_MINUTES", "60"))
    {% endif %}
    
    def get_chat_model(self):
        """Get the configured chat model based on provider"""
        if self.llm_provider == "openai":
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(
                model=self.openai_model,
                api_key=self.openai_api_key
            )
        elif self.llm_provider == "azure_openai":
            from langchain_openai import AzureChatOpenAI
            return AzureChatOpenAI(
                azure_endpoint=self.azure_openai_endpoint,
                api_key=self.azure_openai_api_key,
                api_version=self.azure_openai_api_version,
                deployment_name=self.azure_openai_deployment,
            )
        else:  # ollama
            from langchain_ollama import ChatOllama
            return ChatOllama(
                base_url=self.ollama_base_url,
                model=self.ollama_model
            )
    
    def get_embedding_model(self):
        """Get the configured embedding model based on provider"""
        if self.llm_provider == "openai":
            from langchain_openai import OpenAIEmbeddings
            return OpenAIEmbeddings(
                model=self.openai_embedding_model,
                api_key=self.openai_api_key
            )
        elif self.llm_provider == "azure_openai":
            from langchain_openai import AzureOpenAIEmbeddings
            return AzureOpenAIEmbeddings(
                azure_endpoint=self.azure_openai_endpoint,
                api_key=self.azure_openai_api_key,
                api_version=self.azure_openai_api_version,
                deployment=self.azure_openai_embedding_deployment,
            )
        else:  # ollama
            from langchain_ollama import OllamaEmbeddings
            return OllamaEmbeddings(
                base_url=self.ollama_base_url,
                model=self.ollama_embedding_model
            )


cfg = Config()
