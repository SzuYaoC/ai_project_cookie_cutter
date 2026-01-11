"""
LLM Factory
"""
from app.config import cfg

def get_chat_model():
    """Get the configured chat model based on provider"""
    if cfg.llm_provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=cfg.openai_model,
            api_key=cfg.openai_api_key
        )
    elif cfg.llm_provider == "azure_openai":
        from langchain_openai import AzureChatOpenAI
        return AzureChatOpenAI(
            azure_endpoint=cfg.azure_openai_endpoint,
            api_key=cfg.azure_openai_api_key,
            api_version=cfg.azure_openai_api_version,
            deployment_name=cfg.azure_openai_deployment,
        )
    else:  # ollama
        from langchain_ollama import ChatOllama
        return ChatOllama(
            base_url=cfg.ollama_base_url,
            model=cfg.ollama_model
        )

def get_embedding_model():
    """Get the configured embedding model based on provider"""
    if cfg.llm_provider == "openai":
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(
            model=cfg.openai_embedding_model,
            api_key=cfg.openai_api_key
        )
    elif cfg.llm_provider == "azure_openai":
        from langchain_openai import AzureOpenAIEmbeddings
        return AzureOpenAIEmbeddings(
            azure_endpoint=cfg.azure_openai_endpoint,
            api_key=cfg.azure_openai_api_key,
            api_version=cfg.azure_openai_api_version,
            deployment=cfg.azure_openai_embedding_deployment,
        )
    else:  # ollama
        from langchain_ollama import OllamaEmbeddings
        return OllamaEmbeddings(
            base_url=cfg.ollama_base_url,
            model=cfg.ollama_embedding_model
        )
