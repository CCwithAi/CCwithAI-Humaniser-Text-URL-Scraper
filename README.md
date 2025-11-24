# AI Humaniser

Transform AI-generated text into authentic human-written content using a multi-agent ARCHON system.

> **🚨 IMPORTANT**: This project uses **Archon MCP server** for task management and knowledge base. See [ARCHON_SETUP.md](./ARCHON_SETUP.md) for setup and workflow guide.

## Features

- **Multi-Agent Architecture**: ARCHON-powered pipeline with 5 specialised agents
- **Dual Output Modes**: Sales/Marketing and Journalist/Editorial styles
- **Quality-Driven Iteration**: Automatic refinement until quality threshold met
- **Vector Database**: Supabase-powered human content reference library
- **Modern Stack**: Next.js 15, React 19, Python 3.12, Pydantic AI

## Tech Stack

### Frontend
- Next.js 15.0.3 with App Router
- React 19.0.0
- TypeScript 5.6.3
- shadcn/ui + Tailwind CSS 4.0
- Supabase Client

### Backend
- Python 3.12.7
- Pydantic AI 0.0.14 (ARCHON framework)
- FastAPI 0.115.0
- OpenAI API (GPT-4o-mini)
- Anthropic API (Claude Sonnet 4.5)

### Infrastructure
- Docker Desktop + Docker Compose
- Supabase (PostgreSQL + pgvector)
- MCP (Model Context Protocol) servers

## Project Structure

```
AI Humaniser/
├── frontend/                 # Next.js frontend
│   ├── src/
│   │   ├── app/             # App Router pages
│   │   ├── components/      # React components
│   │   │   └── ui/         # shadcn/ui components
│   │   ├── hooks/          # Custom React hooks
│   │   └── lib/            # Utilities
│   ├── package.json
│   └── tsconfig.json
├── backend/                  # Python backend
│   ├── agents/              # ARCHON agent system
│   │   ├── orchestrator.py
│   │   ├── content_analyser.py
│   │   ├── content_retrieval.py
│   │   ├── style_transformer.py
│   │   └── quality_checker.py
│   ├── models/              # Pydantic models
│   ├── services/            # Business logic
│   ├── main.py              # FastAPI app
│   └── requirements.txt
├── .mcp/                     # MCP configuration
│   └── config.json
├── docker-compose.yml
├── .env.example
└── README.md
```

## ARCHON Agent Flow

```
User Input (AI Text)
    ↓
[1. Content Analyser] - Detects AI patterns
    ↓
[2. Content Retrieval] - Finds similar human writing
    ↓
[3. Style Transformer] - Transforms to human style (Sales/Journalist)
    ↓
[4. Quality Checker] - Validates output
    ↓
[5. Iteration Controller] - Refines if needed (max 3 iterations)
    ↓
Final Human-Like Output
```

## Setup Instructions

### Prerequisites

1. **Docker Desktop** (Windows) - Ensure it's running
2. **Node.js** 22.11.0 LTS or later
3. **Python** 3.12.7 or later
4. **API Keys**:
   - OpenAI API key
   - Anthropic API key
   - Supabase project credentials

### Installation

1. **Clone or navigate to the project:**
   ```bash
   cd "D:\AI Humaniser"
   ```

2. **Configure environment variables:**
   - Copy `.env.example` to `.env`
   - Add your API keys and Supabase credentials:
   ```bash
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key
   OPENAI_API_KEY=sk-your-openai-key
   ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
   ```

3. **Start with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

   This will start:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - MCP servers (docker-compose, context7)

### Alternative: Manual Setup

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

#### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

## Supabase Setup

### 1. Create Supabase Project

Go to [supabase.com](https://supabase.com) and create a new project.

### 2. Create Database Tables

Run this SQL in Supabase SQL Editor:

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Human content table
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

-- Indexes
CREATE INDEX idx_content_type ON human_content(content_type);
CREATE INDEX idx_topic ON human_content(topic);
CREATE INDEX idx_embedding ON human_content USING ivfflat (embedding vector_cosine_ops);

-- Vector similarity search function
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

-- Transformations log table
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
```

### 3. Get API Credentials

From Supabase Project Settings → API:
- Copy `Project URL` → Add to `.env` as `SUPABASE_URL`
- Copy `anon public` key → Add to `.env` as `SUPABASE_KEY`

## API Endpoints

### `POST /api/humanise`
Transform AI text to human writing

**Request:**
```json
{
  "input_text": "Your AI-generated text here...",
  "mode": "sales" // or "journalist"
}
```

**Response:**
```json
{
  "output_text": "Transformed human-like text...",
  "quality_score": 0.87,
  "iterations": 2,
  "mode": "sales",
  "processing_time_ms": 3421,
  "metrics": {
    "burstiness": 0.72,
    "lexical_diversity": 0.68,
    "contraction_ratio": 0.042
  }
}
```

### `GET /api/modes`
Get available transformation modes

### `GET /health`
Health check endpoint

## Usage Example

### Via UI
1. Navigate to http://localhost:3000
2. Paste AI-generated text
3. Select mode: Sales or Journalist
4. Click "Humanise Text"
5. Copy or download result

### Via API
```bash
curl -X POST http://localhost:8000/api/humanise \
  -H "Content-Type: application/json" \
  -d '{
    "input_text": "Furthermore, it is important to note that...",
    "mode": "journalist"
  }'
```

## MCP Integration

The project uses Model Context Protocol (MCP) servers:

- **docker-compose MCP**: Container orchestration
- **Context7 MCP**: Enhanced context window management
- **Supabase MCP**: Direct database integration

Configuration: `.mcp/config.json`

## Development

### Adding Human Content Samples

Place human-written samples in `Human Writen Content/` folder, then index them:

```python
# TODO: Create indexing script
python scripts/index_human_content.py
```

### Testing Agents Individually

```python
from agents.content_analyser import ContentAnalyserAgent

agent = ContentAnalyserAgent()
result = await agent.analyse("Your text here")
print(result)
```

## Quality Metrics

The system evaluates text on:
- **Burstiness**: Sentence length variation
- **Lexical Diversity**: Vocabulary richness
- **Contraction Ratio**: Natural language usage
- **AI Pattern Detection**: Hedge words, formal structures
- **Overall Score**: 0.0-1.0 (target: >0.75)

## Troubleshooting

### Docker issues
- Ensure Docker Desktop is running
- Check port availability (3000, 8000)
- Run `docker-compose down -v` to reset

### API key errors
- Verify `.env` file has valid keys
- Check API credit balance
- Ensure keys are not quoted in `.env`

### Supabase connection
- Verify SUPABASE_URL and SUPABASE_KEY
- Check network connectivity
- Test with mock examples (works without Supabase)

## Roadmap

- [ ] Build main UI components
- [ ] Human content collection script
- [ ] Batch processing endpoint
- [ ] Chrome extension
- [ ] AI detection bypass testing
- [ ] Performance optimisation

## Contributing

This is a private project. For issues or suggestions, contact the project owner.

## License

Proprietary - All rights reserved

---

**Created:** 22nd November 2025
**Status:** Development - Setup Complete
**Next:** Implement UI components and populate human content database
