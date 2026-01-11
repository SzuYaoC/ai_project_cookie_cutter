-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS pgcrypto;

{% if cookiecutter.use_auth == 'yes' %}
-- --------------------------
-- 1) Authentication
-- --------------------------
CREATE TABLE users_info (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create seed users
INSERT INTO users_info (id, username, password_hash, role, created_at)
VALUES (
    gen_random_uuid(),
    'admin',
    'admin',
    'admin',
    NOW()
),
(
    gen_random_uuid(),
    'analyst',
    'analyst',
    'analyst',
    NOW()
),
(
    gen_random_uuid(),
    'support',
    'support',
    'support',
    NOW()
),
(
    gen_random_uuid(),
    'user',
    'user',
    'user',
    NOW()
) ON CONFLICT (username) DO NOTHING;


{% endif %}




-- --------------------------
-- 2) frontend: chainlit
-- --------------------------
{% if cookiecutter.build_frontend == 'yes' %}
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    identifier TEXT NOT NULL UNIQUE,
    metadata JSONB NOT NULL DEFAULT '{}',
    "createdAt" TEXT NOT NULL DEFAULT NOW()
);

CREATE TABLE threads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    "createdAt" TEXT NOT NULL DEFAULT NOW(),
    name TEXT,
    "userId" UUID NOT NULL,
    "userIdentifier" TEXT NOT NULL,
    tags TEXT[],
    metadata JSONB NOT NULL DEFAULT '{}',
    FOREIGN KEY ("userId") REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE steps (
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
    command TEXT,
    start TEXT,
    "end" TEXT,
    generation JSONB,
    "showInput" TEXT,
    language TEXT,
    indent INT,
    "defaultOpen" BOOLEAN,
    FOREIGN KEY ("threadId") REFERENCES threads(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS elements (
    "id" UUID PRIMARY KEY,
    "threadId" UUID,
    "type" TEXT,
    "url" TEXT,
    "chainlitKey" TEXT,
    "name" TEXT NOT NULL,
    "display" TEXT,
    "objectKey" TEXT,
    "size" TEXT,
    "page" INT,
    "language" TEXT,
    "forId" UUID,
    "mime" TEXT,
    "props" JSONB,
    FOREIGN KEY ("threadId") REFERENCES threads("id") ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS feedbacks (
    "id" UUID PRIMARY KEY,
    "forId" UUID NOT NULL,
    "threadId" UUID NOT NULL,
    "value" INT NOT NULL,
    "comment" TEXT,
    FOREIGN KEY ("threadId") REFERENCES threads("id") ON DELETE CASCADE
);
{% endif %}