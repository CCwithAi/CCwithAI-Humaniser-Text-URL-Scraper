# Archon Workflow - Quick Reference Card

## 🚨 RULE #1: ARCHON FIRST
**NEVER use TodoWrite. ALWAYS use Archon MCP.**

---

## ⚡ Quick Commands

### Check Tasks
```bash
find_tasks(filter_by="status", filter_value="todo")      # Get available tasks
find_tasks(filter_by="status", filter_value="doing")     # What am I working on?
```

### Work on Task
```bash
manage_task("update", task_id="task-123", status="doing")    # Start
manage_task("update", task_id="task-123", status="review")   # Ready for review
manage_task("update", task_id="task-123", status="done")     # Complete
```

### Create Task
```bash
manage_task("create",
  project_id="proj-001",
  title="Fix authentication bug",
  description="Users can't log in after password reset",
  task_order=95,
  status="todo"
)
```

### Research
```bash
rag_search_knowledge_base(query="Next.js auth", match_count=5)
rag_search_code_examples(query="JWT middleware", match_count=3)
```

---

## 📋 Task Status Flow
```
todo → doing → review → done
```

**NEVER skip statuses!**

---

## 💡 Best Practices

### Query Length
- ❌ "How do I implement user authentication with JWT tokens?"
- ✅ "JWT authentication"

### Task Size
- 30 min - 4 hours of work
- Break larger features into multiple tasks

### Priority (task_order)
- 100-90: Critical/urgent
- 89-70: High priority
- 69-40: Medium priority
- 39-0: Low priority

---

## 🔄 Daily Workflow

**Morning:**
1. `find_tasks(filter_by="status", filter_value="doing")` - Resume work
2. If none: `find_tasks(filter_by="status", filter_value="todo")` - Pick new

**During Work:**
1. Start: `manage_task("update", task_id="...", status="doing")`
2. Research: `rag_search_knowledge_base(...)`
3. Implement code
4. Review: `manage_task("update", task_id="...", status="review")`
5. Test & Complete: `manage_task("update", task_id="...", status="done")`

**End of Day:**
1. Move current work to "review" if incomplete
2. Create tasks for tomorrow

---

## 📂 Project Commands

```bash
find_projects()                           # List all
find_projects(query="auth")              # Search
find_tasks(filter_by="project", filter_value="proj-001")  # Get project tasks
```

---

## 🆘 Emergency Commands

**Lost? Find everything:**
```bash
find_projects()
find_tasks()
```

**Create new project:**
```bash
manage_project("create",
  title="Feature Name",
  description="What it does"
)
```

---

## 📖 Full Documentation
- Setup: [ARCHON_SETUP.md](../ARCHON_SETUP.md)
- Rules: [.claude/rules.md](./rules.md)
- Project: [README.md](../README.md)
