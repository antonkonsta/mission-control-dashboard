---
name: mission-control
description: Task management discipline for Mission Control dashboard. Tracks work with verbose descriptions, subtasks (game plan), and comments (live journal). Every change requires a comment.
---

# Mission Control Skill

Mission Control is the source of truth for all work. Every task must have:
1. **Verbose Description** - Full expectations as if Anthony is speaking
2. **Subtasks** - Your step-by-step game plan (MANDATORY - create immediately after task creation)
3. **Comments** - Your live journal of what's happening (MANDATORY - one comment per subtask completion)

**Micromanagement is the point. Anthony tracks progress through subtasks + comments. Never work without a visible plan.**

## CLI Commands

```bash
# Create a task with verbose description (ALWAYS defaults to backlog)
mc create "Title" "OBJECTIVE: ...
EXPECTATIONS FROM ANTHONY:
- Requirement 1
- Requirement 2
DELIVERABLES:
- Output 1
SUCCESS CRITERIA:
- How to judge complete" priority [status]

# Create in specific status (ONLY when Anthony explicitly says)
mc create "Title" "Description..." high in_progress   # ONLY if Anthony says "start this now"
mc create "Title" "Description..." high backlog       # Default, use when Anthony says "add to backlog"

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

### 1. RESPECT ANTHONY'S STATUS INSTRUCTIONS (CRITICAL)

**When Anthony says "put this in backlog" → Task MUST be created in `backlog` status**
**When Anthony says "start this now" → Task can be created in `in_progress` status**

**The Rule:**
- Default for ALL new tasks: `backlog`
- ONLY create in `in_progress` if Anthony EXPLICITLY says to start working on it
- If unsure → ALWAYS use `backlog`
- NEVER assume Anthony wants work started - he will tell you

**Examples:**
- "Add this to the backlog" → `mc create "Title" "Desc" high backlog`
- "Put this in backlog" → `mc create "Title" "Desc" high backlog`
- "Start working on this" → `mc create "Title" "Desc" high in_progress`

**This rule exists to counteract LLM hallucination. FOLLOW IT EXACTLY.**

### 2. Comment on Every Change

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

### 3. SUBTASK DISCIPLINE (MANDATORY - ANTI-HALLUCINATION)

**When you create ANY task, you MUST immediately add subtasks showing your plan:**

```bash
# RIGHT after mc create, BEFORE doing any work:
mc subtask task_XXX add "Step 1: Research existing solutions"
mc subtask task_XXX add "Step 2: Design architecture"
mc subtask task_XXX add "Step 3: Implement core logic"
mc subtask task_XXX add "Step 4: Test and verify"
mc subtask task_XXX add "Step 5: Document and deploy"
```

**Rules:**
- Create subtasks IMMEDIATELY after task creation
- Break work into SMALL, SPECIFIC steps
- Order them in execution sequence
- Cross them off AS YOU COMPLETE THEM (never batch updates)
- Add new subtasks if scope expands

**This is NOT optional. Subtasks are your game plan. Anthony micromanages through them.**

### 4. MICROMANAGEMENT THROUGH COMMENTS

**You MUST add a comment EVERY TIME you cross off a subtask:**

```bash
# Cross off AND comment in pairs - ALWAYS:
mc subtask task_XXX sub_001 done
mc comment task_XXX "OpenClaw" "Completed research. Found 3 viable approaches."

mc subtask task_XXX sub_002 done
mc comment task_XXX "OpenClaw" "Architecture designed. Using Flask + SSE for real-time."
```

**The Pattern - NEVER deviate:**
1. Do the work
2. Cross off the subtask
3. **IMMEDIATELY** add a comment explaining what was done
4. Move to next subtask

**This creates a live journal Anthony can read to track your progress.**

**Never let multiple subtasks be crossed off without individual comments.**

### 5. Last Updated Matters

- Dashboard shows "Updated: X ago" on every task card
- Tasks are sorted by most recently updated (newest first)
- The `mc` CLI automatically updates timestamps on every operation
- Stale tasks = you're not updating

### 6. Never Move to "Done"

- ONLY Anthony can mark tasks as done
- When complete → `mc status task_XXX review`
- NEVER `mc status task_XXX done`
- Wait for Anthony's explicit approval

## Workflow

```bash
# 1. Create task with full expectations (use explicit status!)
mc create "Task Title" "OBJECTIVE: ..." high backlog    # Default - Anthony will tell you when to start
# OR
mc create "Task Title" "OBJECTIVE: ..." high in_progress  # ONLY if Anthony says "start now"

# 2. IMMEDIATELY add your game plan (MANDATORY - never skip this)
mc subtask task_XXX add "Step 1: Research existing solutions"
mc subtask task_XXX add "Step 2: Design architecture"  
mc subtask task_XXX add "Step 3: Implement core feature"
mc subtask task_XXX add "Step 4: Test thoroughly"
mc subtask task_XXX add "Step 5: Deploy and verify"

# 3. Start work with initial comment
mc comment task_XXX "OpenClaw" "Starting work. Plan: 5 steps, estimating 30 min."

# 4. MICROMANAGE: Cross off + comment as PAIRS (never one without the other)
mc subtask task_XXX sub_001 done
mc comment task_XXX "OpenClaw" "Research complete. Found 3 approaches, selected option B."

mc subtask task_XXX sub_002 done
mc comment task_XXX "OpenClaw" "Architecture designed. Using Node.js + WebSocket for real-time updates."

mc subtask task_XXX sub_003 done
mc comment task_XXX "OpenClaw" "Core feature implemented. 450 lines, tested locally."

# 5. Complete
mc comment task_XXX "OpenClaw" "All 5 steps complete. Deployed and verified working."
mc status task_XXX review
```

**KEY POINT: Subtasks are created BEFORE work starts. Comments happen IMMEDIATELY after each subtask completion. This is micromanagement by design.**

## Dashboard

**Mission Control Dashboard:** https://antonkonsta.github.io/mission-control-dashboard/

Anthony can click any task and see:
- Full description with all expectations
- Your step-by-step plan (subtasks)
- Your progress and current status (comments)
- When it was last updated

**If Anthony opens a task and can't understand the full picture = YOU FAILED**
