# RAG Project Cookiecutter Template

Generate AI-powered projects from this template.

## Supported Project Types

| Type | Description |
|------|-------------|
| **rag** | Retrieval-Augmented Generation - document search & Q&A with citations |
| **chatbot** | Simple conversational AI without retrieval |
| **agent** | Single AI agent with access to tools |
| **multi_agent** | Multi-agent system with supervisor coordination |

## Usage

```bash
# Install cookiecutter
pip install cookiecutter

# Generate project
cookiecutter ./project_cookie_cutter
```

## Configuration Prompts

| Variable | Options | Description |
|----------|---------|-------------|
| `project_name` | text | Human-readable name |
| `project_type` | rag, chatbot, agent, multi_agent | Type of AI project |
| `llm_provider` | ollama, openai, azure_openai | LLM backend |
| `use_auth` | yes, no | Include JWT auth |
| `include_ingest_server` | yes, no | Include document ingestion |

## Generated Structure

```
{{ project_slug }}/
├── backend/
│   └── app/
│       ├── api/          # Type-specific endpoints
│       ├── rag/          # LangGraph workflows
│       └── config.py     # Multi-provider config
├── frontend/             # Chainlit UI
├── mcp_services/         # MCP tool servers
├── postgres/init/        # DB schema
├── docker-compose.yml
└── .env.example
```
