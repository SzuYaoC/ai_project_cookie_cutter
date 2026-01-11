-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS pgcrypto;
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
{% if cookiecutter.use_auth == 'yes' %}
-- User authentication
CREATE TABLE IF NOT EXISTS users_info (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Default users
INSERT INTO users_info (id, username, password_hash, role, created_at)
VALUES 
    (gen_random_uuid(), 'admin', 'admin', 'admin', NOW()),
    (gen_random_uuid(), 'user', 'user', 'user', NOW())
ON CONFLICT (username) DO NOTHING;
{% endif %}
-- Chainlit tables
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY,
    identifier TEXT NOT NULL UNIQUE,
    metadata JSONB NOT NULL,
    "createdAt" TEXT
);

CREATE TABLE IF NOT EXISTS threads (
    id UUID PRIMARY KEY,
    "createdAt" TEXT,
    name TEXT,
    "userId" UUID,
    "userIdentifier" TEXT,
    tags TEXT[],
    metadata JSONB,
    FOREIGN KEY ("userId") REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS steps (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    "threadId" UUID NOT NULL,
    "parentId" UUID,
    streaming BOOLEAN NOT NULL,
    "waitForAnswer" BOOLEAN,
    "isError" BOOLEAN,
    metadata JSONB,
    tags TEXT[],
    input TEXT,
    output TEXT,
    "createdAt" TEXT,
    FOREIGN KEY ("threadId") REFERENCES threads(id) ON DELETE CASCADE
);
