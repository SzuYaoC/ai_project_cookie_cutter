{% if cookiecutter.project_type == 'rag' %}

CREATE EXTENSION IF NOT EXISTS vector;

-- Documents table
CREATE TABLE IF NOT EXISTS documents (
  id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  regulator      TEXT NOT NULL,
  jurisdiction   TEXT NOT NULL,
  canonical_url  TEXT NOT NULL UNIQUE,
  title          TEXT,
  doc_type       TEXT NOT NULL,
  format         TEXT NOT NULL,
  created_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_documents_reg_jur ON documents (regulator, jurisdiction);

-- Document versions
CREATE TABLE IF NOT EXISTS document_versions (
  id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id    UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  fetched_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
  source_url     TEXT NOT NULL,
  content_sha256 TEXT NOT NULL,
  raw_path       TEXT NOT NULL,
  extracted_path TEXT,
  published_date DATE,
  effective_date DATE,
  version_label  TEXT,
  UNIQUE (document_id, content_sha256)
);

CREATE INDEX IF NOT EXISTS idx_doc_versions_document ON document_versions (document_id);

-- Chunks with embeddings
CREATE TABLE IF NOT EXISTS chunks (
  id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_version_id UUID NOT NULL REFERENCES document_versions(id) ON DELETE CASCADE,
  chunk_index         INT NOT NULL CHECK (chunk_index >= 0),
  section_id          TEXT,
  page_start          INT,
  page_end            INT,
  text                TEXT NOT NULL,
  text_sha256         TEXT NOT NULL,
  token_count         INT,
  headings            TEXT,
  created_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  embedding           vector(768),
  UNIQUE (document_version_id, chunk_index)
);

CREATE INDEX IF NOT EXISTS idx_chunks_docver ON chunks (document_version_id);
CREATE INDEX IF NOT EXISTS idx_chunks_embedding_hnsw ON chunks USING hnsw (embedding vector_cosine_ops);

{% endif %}
