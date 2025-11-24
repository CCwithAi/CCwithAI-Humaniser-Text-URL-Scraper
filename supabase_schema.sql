CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE human_content (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  content TEXT NOT NULL,
  content_type VARCHAR(50) NOT NULL,
  topic VARCHAR(100),
  source_url TEXT,
  author VARCHAR(100),
  published_date DATE,
  emotional_tone VARCHAR(50),
  word_count INTEGER,
  embedding VECTOR(1536),
  created_at TIMESTAMP DEFAULT NOW(),
  metadata JSONB
);

CREATE INDEX idx_content_type ON human_content(content_type);
CREATE INDEX idx_topic ON human_content(topic);
CREATE INDEX idx_embedding ON human_content USING ivfflat (embedding vector_cosine_ops);

CREATE OR REPLACE FUNCTION match_human_content(
  query_embedding VECTOR(1536),
  match_count INT DEFAULT 5,
  content_type_filter VARCHAR DEFAULT NULL
)
RETURNS TABLE (
  id UUID,
  content TEXT,
  content_type VARCHAR,
  topic VARCHAR,
  similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    human_content.id,
    human_content.content,
    human_content.content_type,
    human_content.topic,
    1 - (human_content.embedding <=> query_embedding) AS similarity
  FROM human_content
  WHERE content_type_filter IS NULL OR human_content.content_type = content_type_filter
  ORDER BY human_content.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;

CREATE TABLE transformations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID,
  input_text TEXT NOT NULL,
  output_text TEXT NOT NULL,
  mode VARCHAR(20) NOT NULL,
  quality_score DECIMAL(3,2),
  iterations INTEGER,
  created_at TIMESTAMP DEFAULT NOW(),
  processing_time_ms INTEGER
);

CREATE INDEX idx_transformations_created ON transformations(created_at DESC);
CREATE INDEX idx_transformations_mode ON transformations(mode);
