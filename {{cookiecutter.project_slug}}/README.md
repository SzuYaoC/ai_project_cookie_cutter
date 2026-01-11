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
{% if cookiecutter.include_ingest_server == 'yes' %}
### 4. Ingest Documents

```bash
docker compose exec mcp-ingest python run_pipeline.py
```
{% endif %}
### 5. Access the UI

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
│   ├── search_server/ # Vector search{% if cookiecutter.include_ingest_server == 'yes' %}
│   └── ingest_server/ # Document ingestion{% endif %}
├── postgres/
│   └── init/          # Schema SQL
├── docker-compose.yml
└── .env
```

## License

MIT
