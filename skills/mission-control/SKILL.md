# Mission Control Auto-Sync Skill

**CRITICAL SKILL - Ensures ALL user requests are tracked in Mission Control**

## Purpose

This skill GUARANTEES that every user request is:
1. Added to Mission Control (tasks.json) BEFORE work begins
2. Automatically committed to git
3. Automatically pushed to dashboard remote (GitHub Pages)
4. Visible at https://antonkonsta.github.io/mission-control-dashboard/

## Trigger Conditions

Use this skill for EVERY user request - no exceptions. Including:
- "Can you check X"
- "Look into Y"
- "Research Z"
- Any task, question, or request

## Git Workflow (CRITICAL)

```bash
# After modifying tasks.json:
cd /root/.openclaw/workspace
git add data/tasks.json
git commit -m "Mission Control: <description>"
git push dashboard main  # ← REQUIRED for GitHub Pages update
```

**Two remotes:**
- `origin`: mission-control repo (optional)
- `dashboard`: antonkonsta/mission-control-dashboard (REQUIRED)

## Task Schema

```json
{
  "id": "task_XXX",
  "title": "Short descriptive title",
  "description": "Full description with requirements",
  "status": "backlog|in_progress|review|done",
  "priority": "low|medium|high|critical",
  "subtasks": [
    {
      "id": "sub_001",
      "title": "Subtask description",  // Use "title" NOT "text"
      "done": false
    }
  ],
  "comments": [
    {
      "author": "Name",
      "text": "Comment text",
      "timestamp": "ISO8601"
    }
  ],
  "createdAt": "ISO8601"
}
```

## Usage

### Python Helper (use this for task operations)

```python
import json
from datetime import datetime, timezone

TASKS_FILE = '/root/.openclaw/workspace/data/tasks.json'

def load_tasks():
    with open(TASKS_FILE, 'r') as f:
        return json.load(f)

def save_tasks(data):
    data['lastUpdated'] = datetime.now(timezone.utc).isoformat()
    with open(TASKS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_next_task_id(data):
    existing_ids = [int(t['id'].replace('task_', '')) for t in data['tasks'] if t['id'].startswith('task_')]
    return f"task_{max(existing_ids, default=0) + 1:03d}"

def create_task(title, description, priority='medium', subtasks=None):
    data = load_tasks()
    task_id = get_next_task_id(data)
    
    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "status": "in_progress",
        "priority": priority,
        "subtasks": subtasks or [],
        "comments": [],
        "createdAt": datetime.now(timezone.utc).isoformat()
    }
    
    data['tasks'].append(task)
    save_tasks(data)
    return task_id

def add_comment(task_id, author, text):
    data = load_tasks()
    for task in data['tasks']:
        if task['id'] == task_id:
            task['comments'].append({
                "author": author,
                "text": text,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            break
    save_tasks(data)

def update_subtask(task_id, subtask_id, done=True):
    data = load_tasks()
    for task in data['tasks']:
        if task['id'] == task_id:
            for subtask in task['subtasks']:
                if subtask['id'] == subtask_id:
                    subtask['done'] = done
                    break
            break
    save_tasks(data)

def update_status(task_id, status):
    data = load_tasks()
    for task in data['tasks']:
        if task['id'] == task_id:
            task['status'] = status
            break
    save_tasks(data)
```

### Git Sync (run after EVERY task modification)

```bash
cd /root/.openclaw/workspace && \
git add data/tasks.json && \
git commit -m "Mission Control: <description>" && \
git push dashboard main
```

## Validation Rules

1. **NEVER work on a request without creating a Mission Control task first**
2. **ALWAYS use `title` field for subtasks, NOT `text`**
3. **ALWAYS push to `dashboard` remote after commits**
4. **ALWAYS verify push succeeded before continuing work**

## Dashboard

- URL: https://antonkonsta.github.io/mission-control-dashboard/
- Updates after GitHub Pages build (~1-2 min after push)
- Shows all tasks from `data/tasks.json`
