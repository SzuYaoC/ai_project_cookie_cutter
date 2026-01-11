"""
MCP Search Server
"""
from fastmcp import FastMCP
import os

DATABASE_URL = os.environ.get("DATABASE_URL", "")
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://ollama:11434")
OLLAMA_EMBEDDING_MODEL = os.environ.get("OLLAMA_EMBEDDING_MODEL", "{{ cookiecutter.embedding_model }}")

mcp = FastMCP("search")


@mcp.tool()
def search_chunks(query: str, k: int = 5, filters: dict = None) -> list:
    """
    Search for relevant chunks using vector similarity.
    
    Args:
        query: Search query
        k: Number of results
        filters: Optional filters (regulator, jurisdiction, etc.)
    
    Returns:
        List of matching chunks with scores
    """
    # TODO: Implement vector search
    # 1. Generate query embedding via Ollama
    # 2. Query pgvector with cosine similarity
    # 3. Return top-k results
    return []


@mcp.tool()
def embed_query(text: str) -> list:
    """Generate embedding for a query text"""
    # TODO: Call Ollama embeddings API
    return []


app = mcp.http_app(path="/mcp")
