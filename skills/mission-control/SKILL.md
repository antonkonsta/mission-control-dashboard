---
name: mission-control
description: Task management discipline for Mission Control dashboard. Tracks work with verbose descriptions, subtasks (game plan), and comments (live journal). Every change requires a comment.
---

# Mission Control Skill

Mission Control is the source of truth for all work. Every task must have:
1. **Verbose Description** - Full expectations as if Anthony is speaking
2. **Subtasks** - Your step-by-step game plan
3. **Comments** - Your live journal of what's happening

## CLI Commands

```bash
# Create a task with verbose description
mc create "Title" "OBJECTIVE: ...
EXPECTATIONS FROM ANTHONY:
- Requirement 1
- Requirement 2
DELIVERABLES:
- Output 1
SUCCESS CRITERIA:
- How to judge complete" priority

# Add subtasks (your game plan)
mc subtask task_XXX add "Step 1: Research"
mc subtask task_XXX add "Step 2: Implement"
mc subtask task_XXX add "Step 3: Test"

# Cross off completed subtasks
mc subtask task_XXX sub_001 done

# Add comments (your live journal)
mc comment task_XXX "OpenClaw" "What's happening right now"

# Update status
mc status task_XXX in_progress|review|backlog

# Validate before working
mc validate task_XXX

# Show task details
mc show task_XXX

# List tasks
mc list [status]
```

## 🚨 MANDATORY RULES

### 1. Comment on Every Change

**You MUST add a Mission Control comment whenever you:**
- Cross off a subtask → what was completed
- Add a new subtask → why it was added
- Change task status → why the change
- Make progress → what happened
- Hit a blocker → what the issue is
- Make a decision → the reasoning
- Spawn a sub-agent → the handoff details
- Recover from failure → what you did

**No silent changes. Every action = logged.**

### 2. Subtasks Are Your Game Plan

- Add subtasks BEFORE starting work
- Cross them off AS YOU COMPLETE THEM
- Add new subtasks if scope expands
- Anthony can see your plan at any time

### 3. Last Updated Matters

- Dashboard shows "Updated: X ago" on every task card
- Tasks are sorted by most recently updated (newest first)
- The `mc` CLI automatically updates timestamps on every operation
- Stale tasks = you're not updating

### 4. Never Move to "Done"

- ONLY Anthony can mark tasks as done
- When complete → `mc status task_XXX review`
- NEVER `mc status task_XXX done`
- Wait for Anthony's explicit approval

## Workflow

```bash
# 1. Create task with full expectations
mc create "Task Title" "OBJECTIVE: ..." high

# 2. Add your game plan
mc subtask task_XXX add "Step 1"
mc subtask task_XXX add "Step 2"

# 3. Start work
mc comment task_XXX "OpenClaw" "Starting work..."

# 4. Update as you go
mc subtask task_XXX sub_001 done
mc comment task_XXX "OpenClaw" "Completed step 1, moving to step 2"

# 5. Complete
mc comment task_XXX "OpenClaw" "All deliverables ready"
mc status task_XXX review
```

## Dashboard

**Mission Control Dashboard:** https://antonkonsta.github.io/mission-control-dashboard/

Anthony can click any task and see:
- Full description with all expectations
- Your step-by-step plan (subtasks)
- Your progress and current status (comments)
- When it was last updated

**If Anthony opens a task and can't understand the full picture = YOU FAILED**
