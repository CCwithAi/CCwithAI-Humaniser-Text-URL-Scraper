# AI Humaniser - Initial Project Document

**Created:** 22nd November 2025
**Language:** English UK

## Project Overview

An intelligent system that transforms AI-generated text into authentic human-written content by analysing and replicating the style, tone, word patterns, and emotional expressions found in genuine human writing.

## Core Features

- **Simple UI**: Paste text and process with one click
- **Output Modes**:
  - Sales/Marketing copy
  - Journalist/Editorial content
- **Multi-Agent Processing**: Text flows through specialised AI agents for analysis, transformation, and quality verification
- **Human Content Database**: Indexed repository of authentic human-written content for style reference

---

## Tech Stack (Latest Versions - November 2025)

### Frontend
- **Node.js**: v22.11.0 LTS
- **Next.js**: v15.0.3 (App Router)
- **React**: v19.0.0
- **TypeScript**: v5.6.3
- **shadcn/ui**: Latest (with Radix UI primitives)
- **Tailwind CSS**: v4.0.0

### Backend & AI Agents
- **Python**: v3.12.7
- **Pydantic AI**: v0.0.14 (with ARCHON multi-agent framework)
- **FastAPI**: v0.115.0
- **Langchain**: v0.3.7 (for agent orchestration)

### Database & Storage
- **Supabase**:
  - PostgreSQL v15.1
  - Supabase Client (JS): v2.45.4
  - Supabase Client (Python): v2.9.1
  - Supabase Vector: pgvector v0.7.0

### Infrastructure
- **Docker Desktop**: v4.35.1 (Windows)
- **Docker Compose**: v2.29.0
- **MCP (Model Context Protocol)**: Existing Docker MCP servers

---

## Architecture: ARCHON Multi-Agent System

### Agent Flow

```
User Input (AI Text)
    ↓
[Content Analyser Agent]
    ↓
[Human Content Retrieval Agent] ←→ [Supabase Vector DB]
    ↓
[Style Transformer Agent] (Sales OR Journalist mode)
    ↓
[Quality Checker Agent]
    ↓
[Iteration Controller] → Feedback Loop (if quality < threshold)
    ↓
Final Human-Like Output
```

### ARCHON Agents

#### 1. **Content Analyser Agent**
- **Role**: Analyse input text characteristics
- **Tasks**:
  - Detect AI-generated patterns (repetitive phrasing, formal structure)
  - Identify content type and topic
  - Determine required transformation depth

#### 2. **Human Content Retrieval Agent**
- **Role**: Database manager for human-written content
- **Tasks**:
  - Index human content by: content type, topic, date, emotional tone
  - Perform vector similarity search
  - Retrieve relevant style examples
- **Data Sources**:
  - Journalist: BBC, Guardian, local news outlets
  - Sales: Marketing emails, landing pages, social media
  - Blog: Medium, Substack articles
  - Scientific: Journal articles, research papers

#### 3. **Style Transformer Agent** (Mode-Specific)
- **Role**: Transform AI text to human style
- **Tasks**:
  - Apply human writing patterns from database
  - Inject natural variations, contractions, colloquialisms
  - Add emotional authenticity and personal voice
  - Remove AI-telltale signs (over-politeness, excessive structure)

**Sales Mode Characteristics**:
- Conversational tone
- Persuasive language
- Call-to-action focus
- Benefit-driven phrasing
- Personal pronouns (you, we, your)

**Journalist Mode Characteristics**:
- Objective reporting
- Active voice preference
- Proper attribution
- Inverted pyramid structure
- Engaging hooks and transitions

#### 4. **Quality Checker Agent**
- **Role**: Validate human-like quality
- **Tasks**:
  - Score against human writing metrics
  - Check for remaining AI patterns
  - Verify tone consistency
  - Assess readability (Flesch-Kincaid, etc.)

#### 5. **Iteration Controller Agent**
- **Role**: Orchestrate refinement cycles
- **Tasks**:
  - Evaluate Quality Checker feedback
  - Trigger re-processing if needed (max 3 iterations)
  - Approve final output

---

## Database Schema (Supabase)

### Table: `human_content`
```sql
CREATE TABLE human_content (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  content TEXT NOT NULL,
  content_type VARCHAR(50) NOT NULL, -- 'journalist', 'sales', 'blog', 'social_media', 'scientific'
  topic VARCHAR(100),
  source_url TEXT,
  author VARCHAR(100),
  published_date DATE,
  emotional_tone VARCHAR(50), -- 'neutral', 'persuasive', 'informative', 'conversational'
  word_count INTEGER,
  embedding VECTOR(1536), -- OpenAI embeddings or similar
  created_at TIMESTAMP DEFAULT NOW(),
  metadata JSONB
);

CREATE INDEX idx_content_type ON human_content(content_type);
CREATE INDEX idx_topic ON human_content(topic);
CREATE INDEX idx_embedding ON human_content USING ivfflat (embedding vector_cosine_ops);
```

### Table: `transformations`
```sql
CREATE TABLE transformations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID,
  input_text TEXT NOT NULL,
  output_text TEXT NOT NULL,
  mode VARCHAR(20) NOT NULL, -- 'sales', 'journalist'
  quality_score DECIMAL(3,2),
  iterations INTEGER,
  created_at TIMESTAMP DEFAULT NOW(),
  processing_time_ms INTEGER
);
```

---

## MCP Integration (Docker Desktop)

### MCP Configuration File
**Location**: `.mcp/config.json`

```json
{
  "mcpServers": {
    "docker-compose": {
      "command": "docker",
      "args": ["exec", "mcp-server", "mcp-docker-compose"],
      "env": {
        "COMPOSE_PROJECT_NAME": "ai-humaniser"
      }
    },
    "context7": {
      "command": "docker",
      "args": ["exec", "mcp-context7", "mcp-context"],
      "env": {
        "CONTEXT_WINDOW": "7"
      }
    },
    "supabase-mcp": {
      "command": "docker",
      "args": ["exec", "mcp-supabase", "mcp-supabase-client"],
      "env": {
        "SUPABASE_URL": "${SUPABASE_URL}",
        "SUPABASE_ANON_KEY": "${SUPABASE_ANON_KEY}"
      }
    }
  }
}
```

### Docker Compose Services
**File**: `docker-compose.yml`

```yaml
version: '3.8'

services:
  frontend:
    image: node:22.11.0-alpine
    working_dir: /app
    volumes:
      - ./frontend:/app
    ports:
      - "3000:3000"
    command: npm run dev
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000

  backend:
    image: python:3.12.7-slim
    working_dir: /app
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}

  mcp-server:
    image: modelcontextprotocol/server:latest
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    networks:
      - ai-humaniser-network

  mcp-context7:
    image: modelcontextprotocol/context7:latest
    networks:
      - ai-humaniser-network

networks:
  ai-humaniser-network:
    driver: bridge
```

---

## Environment Variables

**File**: `.env`

```bash
# Supabase (Placeholder - Replace with your credentials)
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_KEY=your-service-key-here

# AI Model APIs
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000

# Docker MCP
MCP_DOCKER_HOST=/var/run/docker.sock
CONTEXT7_ENABLED=true
```

---

## User Interface (Simple Paste & Process)

### Main Components

#### 1. **Input Panel**
- Large textarea for pasting AI-generated text
- Character count display
- Clear button

#### 2. **Mode Selector**
- Toggle/Button group: **Sales** | **Journalist**
- Visual indicator of selected mode

#### 3. **Process Button**
- Single "Humanise Text" action button
- Loading state with progress indicator
- Shows iteration count during processing

#### 4. **Output Panel**
- Display transformed human-like text
- Copy to clipboard button
- Quality score badge
- Download as .txt option

#### 5. **Diff Viewer** (Optional)
- Side-by-side or inline comparison
- Highlights changes made

### UI Framework (shadcn/ui Components)
- `Textarea` - Input/Output text areas
- `Button` - Action buttons
- `Card` - Content containers
- `Badge` - Quality score, mode indicator
- `Tabs` - Mode selection
- `Progress` - Loading state
- `Toast` - Success/error notifications

---

## Development Workflow

### Phase 1: Setup (Week 1)
1. Initialize Next.js project with TypeScript
2. Setup Supabase database and tables
3. Configure Docker Compose environment
4. Install shadcn/ui components
5. Setup MCP connections

### Phase 2: Human Content Collection (Week 1-2)
1. Scrape/collect human-written samples
2. Process and vectorise content
3. Store in Supabase with metadata
4. Build retrieval system

### Phase 3: ARCHON Agent Development (Week 2-3)
1. Implement Content Analyser Agent
2. Implement Human Content Retrieval Agent
3. Implement Style Transformer Agents (Sales & Journalist)
4. Implement Quality Checker Agent
5. Implement Iteration Controller

### Phase 4: Frontend Development (Week 3-4)
1. Build UI components
2. Integrate API calls
3. Add real-time feedback
4. Polish UX/UI

### Phase 5: Testing & Refinement (Week 4-5)
1. Test with various AI-generated inputs
2. Refine agent prompts and logic
3. Optimise quality metrics
4. Performance testing

---

## Key Differences: AI Writing vs Human Writing

### AI-Generated Characteristics (TO ELIMINATE)
- Overly structured paragraphs
- Excessive use of "Moreover", "Furthermore", "In conclusion"
- Repetitive sentence structures
- Formal/stiff tone
- Predictable word choices
- Lack of personal voice
- Over-explanation
- Perfectly balanced arguments

### Human Writing Characteristics (TO REPLICATE)
- Natural flow with varied sentence lengths
- Contractions and colloquialisms
- Personal anecdotes and opinions
- Emotional authenticity
- Imperfect grammar (occasional fragments, run-ons)
- Unique word associations
- Subjectivity and bias (when appropriate)
- Unexpected transitions
- Cultural references
- Humour and personality

---

## Quality Metrics

### Automated Checks
1. **Perplexity Score**: Lower = more predictable (AI-like)
2. **Burstiness**: Variation in sentence length/complexity
3. **Lexical Diversity**: Unique word ratio
4. **Sentiment Consistency**: Natural emotional flow
5. **AI Detection Tools**: Zero-GPT, GPTZero scores

### Target Scores
- Human-likeness: > 85%
- AI Detection: < 15% probability
- Readability: Flesch Reading Ease 60-70 (Standard)
- Engagement: Headline Analyser 70+

---

## Next Steps

1. **Set up Supabase project** and obtain API credentials
2. **Initialize Next.js frontend** with shadcn/ui
3. **Build Python backend** with Pydantic AI + ARCHON
4. **Configure Docker MCP** connections
5. **Collect initial human content** samples (50+ per category)
6. **Implement first agent** (Content Analyser)
7. **Build MVP UI** (paste, process, output)

---

## Resources

- [Pydantic AI Documentation](https://ai.pydantic.dev/)
- [ARCHON Framework](https://ai.pydantic.dev/agents/)
- [shadcn/ui Components](https://ui.shadcn.com/)
- [Supabase Vector Documentation](https://supabase.com/docs/guides/ai)
- [MCP Protocol Specification](https://modelcontextprotocol.io/)
- [Context7 Documentation](https://context7.ai/)

---

**Project Status:** Planning → Ready for Implementation

**Estimated Timeline:** 5 weeks to MVP

**Team Requirements:**
- 1x Full-stack Developer (Next.js + Python)
- 1x AI/ML Engineer (Agent development)
- 1x Content Specialist (Human writing samples)
