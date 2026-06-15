-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Users (mirrors Supabase auth.users)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    name TEXT,
    phone TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Crop disease detection history
CREATE TABLE IF NOT EXISTS crop_images (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    image_url TEXT NOT NULL,
    crop TEXT,
    disease TEXT,
    confidence FLOAT,
    treatment TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Fertilizer recommendation history
CREATE TABLE IF NOT EXISTS fertilizer_predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    crop TEXT NOT NULL,
    nitrogen FLOAT,
    phosphorus FLOAT,
    potassium FLOAT,
    ph FLOAT,
    result JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Yield prediction history
CREATE TABLE IF NOT EXISTS yield_predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    state TEXT,
    district TEXT,
    crop TEXT,
    area FLOAT,
    result JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Chat history
CREATE TABLE IF NOT EXISTS chat_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    language TEXT DEFAULT 'hi',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- RAG Knowledge base
CREATE TABLE IF NOT EXISTS knowledge_base (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    embedding vector(384),
    category TEXT,
    language TEXT DEFAULT 'hi',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Vector index for fast similarity search
CREATE INDEX IF NOT EXISTS kb_embedding_idx
    ON knowledge_base USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);
