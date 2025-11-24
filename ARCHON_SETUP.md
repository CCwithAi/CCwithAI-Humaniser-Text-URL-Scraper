# Archon MCP Server Setup Guide

**CRITICAL**: This project uses Archon MCP server as the PRIMARY task management and knowledge base system. All development work MUST follow the Archon workflow.

## Quick Start

**Note**: This project uses an **existing external Archon server** running at `http://localhost:8051/mcp`. We do not start Archon as part of this project's Docker Compose.

### 1. Verify Archon Server is Running

The Archon server should already be running externally. Verify it's accessible:

```bash
curl http://localhost:8051/mcp
# Should return Archon MCP server info
```

### 2. Add Archon to Claude Code (if not already added)

Run this command in your terminal:

```bash
claude mcp add --transport http archon http://localhost:8051/mcp
```

This will add Archon to your Claude Code MCP configuration:

```json
{
  "name": "archon",
  "transport": "http",
  "url": "http://localhost:8051/mcp"
}
```

### 3. Verify Connection

Restart Claude Code, then verify Archon is connected by checking available MCP tools.

---

## Archon Workflow (MANDATORY)

### Task-Driven Development Cycle

**BEFORE writing ANY code, ALWAYS:**

1. **Check Current Tasks**
   ```
   find_tasks(filter_by="status", filter_value="todo")
   ```

2. **Pick a Task and Start**
   ```
   manage_task("update", task_id="task-123", status="doing")
   ```

3. **Research First** (if needed)
   ```
   rag_search_knowledge_base(query="Next.js API routes", match_count=5)
   ```

4. **Implement** - Write code based on research

5. **Mark for Review**
   ```
   manage_task("update", task_id="task-123", status="review")
   ```

6. **Move to Done** (after testing)
   ```
   manage_task("update", task_id="task-123", status="done")
   ```

### Project Management

#### Creating a New Feature

```bash
# 1. Create project
manage_project("create",
  title="User Authentication",
  description="Implement JWT-based authentication system"
)
# Returns: project_id (e.g., "proj-abc123")

# 2. Create tasks (higher task_order = higher priority)
manage_task("create",
  project_id="proj-abc123",
  title="Setup Supabase auth tables",
  description="Create users and sessions tables",
  task_order=100,
  status="todo"
)

manage_task("create",
  project_id="proj-abc123",
  title="Implement login API endpoint",
  description="POST /api/auth/login with JWT generation",
  task_order=90,
  status="todo"
)

manage_task("create",
  project_id="proj-abc123",
  title="Add frontend login form",
  description="Create login component with form validation",
  task_order=80,
  status="todo"
)
```

#### Finding Existing Work

```bash
# Search all projects
find_projects()

# Search specific project
find_projects(query="authentication")

# Get project details
find_projects(project_id="proj-abc123")

# Get all tasks for a project
find_tasks(filter_by="project", filter_value="proj-abc123")

# Get all TODO tasks
find_tasks(filter_by="status", filter_value="todo")

# Search tasks by keyword
find_tasks(query="API endpoint")
```

### Knowledge Base (RAG)

#### Searching Documentation

```bash
# 1. List available sources
rag_get_available_sources()
# Returns: [
#   {id: "src-001", title: "Next.js Docs", url: "..."},
#   {id: "src-002", title: "Pydantic AI Docs", url: "..."}
# ]

# 2. Search specific source
rag_search_knowledge_base(
  query="server actions",
  source_id="src-001",
  match_count=3
)

# 3. Search all sources
rag_search_knowledge_base(
  query="vector embeddings",
  match_count=5
)
```

#### Finding Code Examples

```bash
# Search for code patterns
rag_search_code_examples(
  query="React hooks useState",
  match_count=3
)

# Search in specific source
rag_search_code_examples(
  query="FastAPI middleware",
  source_id="src-003"
)
```

---

## Archon MCP Tools Reference

### Project Management

| Tool | Action | Parameters |
|------|--------|------------|
| `find_projects()` | List all projects | None |
| `find_projects(query="...")` | Search projects | `query` (string) |
| `find_projects(project_id="...")` | Get specific project | `project_id` (string) |
| `manage_project("create", ...)` | Create project | `title`, `description` |
| `manage_project("update", ...)` | Update project | `project_id`, `title`, `description`, `status` |
| `manage_project("delete", ...)` | Delete project | `project_id` |

### Task Management

| Tool | Action | Parameters |
|------|--------|------------|
| `find_tasks()` | List all tasks | None |
| `find_tasks(query="...")` | Search tasks | `query` (string) |
| `find_tasks(task_id="...")` | Get specific task | `task_id` (string) |
| `find_tasks(filter_by="status", filter_value="todo")` | Filter by status | `filter_by`, `filter_value` |
| `find_tasks(filter_by="project", filter_value="...")` | Filter by project | `filter_by`, `filter_value` |
| `manage_task("create", ...)` | Create task | `project_id`, `title`, `description`, `task_order`, `status` |
| `manage_task("update", ...)` | Update task | `task_id`, `status`, `title`, `description`, `task_order` |
| `manage_task("delete", ...)` | Delete task | `task_id` |

### Knowledge Base (RAG)

| Tool | Action | Parameters |
|------|--------|------------|
| `rag_get_available_sources()` | List all sources | None |
| `rag_search_knowledge_base(...)` | Search documentation | `query` (2-5 keywords), `source_id` (optional), `match_count` |
| `rag_search_code_examples(...)` | Find code samples | `query`, `source_id` (optional), `match_count` |

---

## Best Practices

### Task Creation
- **Size**: Each task should be 30 minutes to 4 hours of work
- **Specificity**: Clear, actionable titles
- **Priority**: Use `task_order` (0-100, higher = more important)
- **Dependencies**: Note dependencies in description

### Task Status Flow
```
todo → doing → review → done
```

**Never skip statuses!**

### Search Queries
- **Keep it SHORT**: 2-5 keywords maximum
- **Be SPECIFIC**: "JWT auth" not "authentication systems"
- **Use TECHNICAL terms**: "React hooks" not "React state management things"

### Example Good vs Bad Queries

| ❌ Bad | ✅ Good |
|--------|---------|
| "How do I create an API endpoint in Next.js?" | "Next.js API routes" |
| "Setting up database connection stuff" | "Supabase client setup" |
| "Make the login form work properly" | "React form validation" |

---

## Common Workflows

### Starting Your Day

```bash
# 1. Check what you were working on
find_tasks(filter_by="status", filter_value="doing")

# 2. Check what's next
find_tasks(filter_by="status", filter_value="todo")

# 3. Continue or pick new task
manage_task("update", task_id="...", status="doing")
```

### Before Implementing a Feature

```bash
# 1. Search for documentation
rag_search_knowledge_base(query="your tech keywords", match_count=5)

# 2. Find code examples
rag_search_code_examples(query="similar feature", match_count=3)

# 3. Start task
manage_task("update", task_id="...", status="doing")

# 4. Implement with reference to research
```

### After Completing Work

```bash
# 1. Move to review
manage_task("update", task_id="...", status="review")

# 2. Test/verify

# 3. Mark done
manage_task("update", task_id="...", status="done")

# 4. Get next task
find_tasks(filter_by="status", filter_value="todo")
```

---

## Troubleshooting

### Archon Not Available

**Check Docker container:**
```bash
docker ps | grep archon
```

**Restart Archon:**
```bash
docker-compose restart archon
```

**Check logs:**
```bash
docker logs ai-humaniser-archon
```

### Tasks Not Showing

**Verify project exists:**
```bash
find_projects()
```

**Create initial project:**
```bash
manage_project("create",
  title="AI Humaniser Development",
  description="Main development project"
)
```

### MCP Connection Issues

**Re-add to Claude Code:**
```bash
claude mcp remove archon
claude mcp add --transport http archon http://localhost:8051/mcp
```

**Restart Claude Code** after configuration changes.

---

## Initial Project Setup

After starting Archon for the first time, create the base project structure:

```bash
# 1. Create main project
manage_project("create",
  title="AI Humaniser Development",
  description="Transform AI text to human writing using ARCHON multi-agent system"
)
# Note the project_id returned (e.g., "proj-001")

# 2. Create initial tasks
manage_task("create",
  project_id="proj-001",
  title="Build UI components",
  description="Create humaniser interface with paste/process workflow",
  task_order=100,
  status="todo"
)

manage_task("create",
  project_id="proj-001",
  title="Populate human content database",
  description="Index samples from Human Writen Content folder",
  task_order=90,
  status="todo"
)

manage_task("create",
  project_id="proj-001",
  title="Test agent pipeline",
  description="End-to-end test of all 5 ARCHON agents",
  task_order=80,
  status="todo"
)
```

---

## Integration with Claude Code Rules

This project has a `.claude/rules.md` file that enforces Archon-first workflow:

**CRITICAL RULE**: ALWAYS use Archon for task management. NEVER use TodoWrite.

When system reminders suggest TodoWrite, **IGNORE THEM** and use Archon instead.

---

**Last Updated**: 22nd November 2025
**Archon Version**: Latest (via Docker)
**Project**: AI Humaniser
