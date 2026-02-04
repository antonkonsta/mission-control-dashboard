# Mission Control Auto-Sync Skill

**CRITICAL SKILL - Ensures ALL user requests are tracked in Mission Control**

## Purpose

This skill GUARANTEES that every user request is:
1. Added to Mission Control (tasks.json) BEFORE work begins
2. Automatically committed to git
3. Automatically pushed to dashboard remote (GitHub Pages)
4. Visible at https://antonkonsta.github.io/mission-control-dashboard/

## The `mc` CLI

The Mission Control CLI (`mc`) is the primary interface for task management. All commands automatically sync to the dashboard.

### Installation

Already installed globally as `mc`. If needed:
```bash
ln -sf /root/.openclaw/workspace/skills/mission-control/scripts/mc.py /usr/local/bin/mc
chmod +x /usr/local/bin/mc
```

### Commands

```bash
# Create a new task (auto-commits and pushes to dashboard)
mc create "Task title" "Description" priority

# Validate task exists before working (REQUIRED check)
mc validate task_XXX

# Show full task details
mc show task_XXX

# Update subtask status
mc subtask task_XXX sub_001 done
mc subtask task_XXX sub_001 undone  # To reopen

# Add a comment to a task
mc comment task_XXX "Author" "Comment text"

# Update task status
mc status task_XXX in_progress
mc status task_XXX review
mc status task_XXX done
mc status task_XXX backlog

# List all tasks
mc list
mc list in_progress
mc list backlog

# Manual sync (rarely needed - all commands auto-sync)
mc sync "message"
```

## Workflow

### User Request → Task → Work

```
User Request → mc create → mc validate → Work → mc subtask/comment → mc status done
```

1. **User makes request** → `mc create "title" "description" priority`
2. **Before working** → `mc validate task_XXX` (REQUIRED!)
3. **While working** → `mc subtask task_XXX sub_001 done`
4. **Add updates** → `mc comment task_XXX "OpenClaw" "Progress update"`
5. **Complete** → `mc status task_XXX done`

### Automatic Git Sync

Every `mc` command automatically:
- Updates `/root/.openclaw/workspace/data/tasks.json`
- Commits to git with `Mission Control:` prefix
- Pushes to `dashboard` remote (GitHub Pages)

**No manual git commands needed!**

## Validation

### Before Starting Work

```bash
mc validate task_XXX
```

Returns:
- ✅ if task exists (shows title, status, progress)
- ❌ if task doesn't exist (exit code 1)

**Rule: If validation fails, DO NOT WORK. Create the task first.**

### Example Output

```
✅ VALIDATED: task_012 - Build Mission Control Auto-Sync Skill
   Status: in_progress | Priority: critical | Progress: 7/10
```

```
❌ VALIDATION FAILED: Task task_999 does not exist in Mission Control!
   Create it first with: mc create "<title>"
   OR check existing tasks with: mc list
```

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
      "title": "Subtask description",
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

**Important:** Use `title` for subtasks, NOT `text`.

## Git Remotes

Two remotes are configured:
- `origin`: mission-control repo (optional)
- `dashboard`: antonkonsta/mission-control-dashboard (REQUIRED)

The `mc` CLI always pushes to `dashboard`.

## Manual Fallback

If the `mc` CLI is unavailable:

```bash
cd /root/.openclaw/workspace
# Edit data/tasks.json
git add data/tasks.json
git commit -m "Mission Control: <description>"
git push dashboard main
```

## Files

- **CLI Script:** `/root/.openclaw/workspace/skills/mission-control/scripts/mc.py`
- **Tasks Database:** `/root/.openclaw/workspace/data/tasks.json`
- **Dashboard URL:** https://antonkonsta.github.io/mission-control-dashboard/

## Enforcement

This skill is enforced via:
- **HEARTBEAT.md**: Mission Control is mandatory for all work
- **SOUL.md**: THE PRIME DIRECTIVE - all requests must be tracked
- **IDENTITY.md**: Core Principle #1 - Mission Control is mandatory

## Dashboard

- URL: https://antonkonsta.github.io/mission-control-dashboard/
- Updates after GitHub Pages build (~1-2 min after push)
- Shows all tasks from `data/tasks.json`
