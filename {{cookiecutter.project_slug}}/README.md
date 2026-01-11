# {{ cookiecutter.project_name }}

{{ cookiecutter.description }}

## Quick Start

### Prerequisites
- Docker & Docker Compose
- ~8GB RAM for Ollama models

### 1. Configure Environment

```bash
cp .env.example .env
# Edit .env with your settings
```

### 2. Start Services

```bash
docker compose up --build
```

### 3. Pull LLM Models

```bash
docker compose exec ollama ollama pull {{ cookiecutter.ollama_model }}
docker compose exec ollama ollama pull {{ cookiecutter.embedding_model }}
```
{% if cookiecutter.project_type == 'rag' %}
### 4. Ingest Documents

```bash
docker compose exec mcp-ingest python run_pipeline.py
```
{% endif %}
### {% if cookiecutter.project_type == 'rag' %}5{% else %}4{% endif %}. Access the UI

Open http://localhost:8081

## Architecture

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Chainlit  │──────▶   FastAPI   │──────▶  MCP Search │
│    :8081    │      │    :8000    │      │    :7071    │
└─────────────┘      └─────────────┘      └─────────────┘
                            │                    │
                            ▼                    ▼
                     ┌─────────────┐      ┌─────────────┐
                     │   Ollama    │      │  PostgreSQL │
                     │   :11434    │      │    :5432    │
                     └─────────────┘      └─────────────┘
```

## Project Structure

```
├── backend/           # FastAPI + LangGraph
├── frontend/          # Chainlit UI
├── mcp_services/
│   ├── search_server/ # Vector search{% if cookiecutter.project_type == 'rag' %}
│   └── ingest_server/ # Document ingestion{% endif %}
├── postgres/
│   └── init/          # Schema SQL
├── docker-compose.yml
└── .env
```

## License

MIT
