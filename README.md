# AI Project Cookiecutter Template

Generate AI-powered projects from this template.

## Project Types

| Type | MCP Services | Description |
|------|--------------|-------------|
| **rag** | `search_server`, `ingest_server` | Document search & Q&A with citations |
| **chatbot** | `memory_server` | Conversational AI with history |
| **agent** | `tools_server` | AI agent with tools (web search, code, etc.) |
| **multi_agent** | `tools_server`, `coordination_server` | Multi-agent system with coordination |

## Usage

```bash
# Install cookiecutter (or use uvx)
pipx install cookiecutter

# Generate project
cookiecutter ./ai_project_cookiecutter

# Or with uv
uvx cookiecutter ./ai_project_cookiecutter
```

## Configuration Prompts

| Variable | Options | Description |
|----------|---------|-------------|
| `project_name` | text | Human-readable name |
| `project_type` | rag, chatbot, agent, multi_agent | Type of AI project |
| `llm_provider` | ollama, openai, azure_openai | LLM backend |
| `use_auth` | yes, no | Include JWT authentication |

## Generated Structure

```
{{ project_slug }}/
├── backend/
│   └── app/
│       ├── api/          # Type-specific endpoints
│       ├── rag/          # LangGraph workflows  
│       └── config.py     # Multi-provider config
├── frontend/             # Chainlit UI
├── mcp_services/         # Type-specific MCP servers
├── postgres/init/        # DB schema
├── docker-compose.yml
└── .env.example
```

## MCP Services by Type

### RAG
- **search_server** - Vector similarity search
- **ingest_server** - Document ingestion pipeline

### Chatbot
- **memory_server** - Conversation history management

### Agent
- **tools_server** - Web search, URL fetch, code execution

### Multi-Agent
- **tools_server** - Shared tools for all agents
- **coordination_server** - Task management, inter-agent messaging
