---
name: mission-control
description: Task management discipline for Mission Control dashboard. Tracks work with verbose descriptions, subtasks (game plan), and comments (live journal). Every change requires a comment.
---

# Mission Control Skill

Mission Control is the source of truth for all work. Every task must have:
1. **Verbose Description** - Full expectations as if Anthony is speaking
2. **Subtasks** - Your researched step-by-step game plan (MANDATORY - research FIRST, then create specific steps)
3. **Comments** - Your live journal of what's happening (MANDATORY - one comment per subtask completion)

**Research comes FIRST. Subtasks are your researched plan, not generic guesses. Anthony tracks progress through subtasks + comments. Never work without a visible, researched plan.**

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

### 3. SUBTASK DISCIPLINE (MANDATORY - RESEARCH FIRST)

**When you create ANY task, you MUST do research BEFORE adding subtasks:**

```bash
# RESEARCH PHASE (do this FIRST before adding subtasks):
# 1. Read existing code/docs related to the task
# 2. Search codebase for relevant files, functions, patterns
# 3. Look at similar implementations
# 4. Understand what files need to be created/modified
# 5. Identify dependencies, blockers, prerequisites
# 6. Estimate actual effort based on research

# THEN add specific, researched subtasks:
mc subtask task_XXX add "Step 1: Research existing solutions"
mc subtask task_XXX add "Step 2: Design architecture"
mc subtask task_XXX add "Step 3: Implement core logic"
mc subtask task_XXX add "Step 4: Test and verify"
mc subtask task_XXX add "Step 5: Document and deploy"
```

**Rules:**
- **RESEARCH FIRST**: Investigate codebase, docs, existing solutions BEFORE creating subtasks
- Subtasks must reflect ACTUAL implementation steps, not generic summaries
- Look at files, understand what needs to change, then document the plan
- Break work into SMALL, SPECIFIC, RESEARCHED steps
- Order them in execution sequence
- Cross them off AS YOU COMPLETE THEM (never batch updates)
- **UPDATE subtasks as you learn**: Add new ones, modify existing ones when discovery happens
- Research is part of the work - document what you found in comments

**This is NOT optional. Subtasks are your researched game plan. Anthony micromanages through them.**

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

### 6. WORKFLOW & STATUS DEFINITIONS (READ EVERY TIME)

**YOU HAVE AMNESIA. YOU CANNOT REMEMBER CONTEXT. READ THIS EVERY USE.**

#### ANTHONY'S EXACT COMMANDS:

| Anthony Says | You Do | Result |
|--------------|--------|--------|
| **"Remove it"** / **"Delete it"** | `mc remove task_XXX` | Task DELETED forever |
| **"Move to backlog"** | `mc status task_XXX backlog` | Task exists, not started |
| **"Move to in_progress"** / **"Start this"** | `mc status task_XXX in_progress` + **DELEGATE** | **WORK BEGINS** |
| **"Move to review"** | `mc status task_XXX review` | Work done, await approval |
| **"Mark done"** | Tell Anthony only he can | **NEVER YOU** |

#### THE WORKFLOW (NEVER DEVIATE):

```
BACKLOG → IN_PROGRESS → REVIEW → DONE
   ↑          ↑            ↑        ↑
   │          │            │        └── ONLY ANTHONY
   │          │            └── You move when sub-agents complete ALL subtasks
   │          └── You move here, IMMEDIATELY SPAWN SUB-AGENTS
   └── ALL tasks start here
```

#### STATUS MEANINGS:

- **backlog** → Task exists, no work started, no sub-agents
- **in_progress** → Sub-agents actively working (you supervise)
- **review** → Sub-agents finished all subtasks, await Anthony
- **done** → Anthony approved (NEVER set this yourself)

#### "REMOVE" = DELETE (NOT BACKLOG)

**When Anthony says "remove":**
- ❌ WRONG: `mc status task_XXX backlog` 
- ✅ RIGHT: `mc remove task_XXX` (task gone forever)

**When Anthony says "move to backlog":**
- ✅ RIGHT: `mc status task_XXX backlog`

**NEVER confuse these. "Remove" means ERASE. "Backlog" means save for later.**

#### IN_PROGRESS = DELEGATE IMMEDIATELY

**When task is `in_progress`:**
1. **YOU DO NOT WORK ON IT**
2. **SPAWN SUB-AGENTS** with label matching task ID
3. **SUPERVISE** every 2 minutes via sessions_list + sessions_send
4. **WHIP SUB-AGENTS** - demand status, kill if stuck
5. **When ALL subtasks complete** → move to `review`
6. **Report to Anthony** - "Task_XXX: All subtasks done, moved to review"

**NEVER FORGET:**
- Main session NEVER implements - only manages
- Sub-agents do ALL work
- You have NO MEMORY - re-read this every time

### 7. Never Move to "Done"

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

# 2. RESEARCH PHASE (MANDATORY - do this before adding subtasks)
#    - Read existing code in relevant directories
#    - Search for similar implementations
#    - Understand current architecture
#    - Identify what files need changes
#    - Look at docs, skills, examples
# mc comment task_XXX "OpenClaw" "Researching codebase. Found monitor_server.py, 
#    existing logs in /var/log/openclaw/, and transcript files in sessions/."

# 3. THEN add researched game plan (specific steps based on research)
mc subtask task_XXX add "Step 1: Read existing Activity Monitor implementation"
mc subtask task_XXX add "Step 2: Analyze log file formats and data structures"
mc subtask task_XXX add "Step 3: Design new data collection endpoint"
mc subtask task_XXX add "Step 4: Implement real-time SSE streaming"
mc subtask task_XXX add "Step 5: Build frontend dashboard components"
mc subtask task_XXX add "Step 6: Test with live agent sessions"
mc comment task_XXX "OpenClaw" "Research complete. Plan based on existing Flask server 
    in monitor_server.py. Will extend with SSE and new routes."

# 4. MICROMANAGE: Cross off + comment as PAIRS (never one without the other)
mc subtask task_XXX sub_001 done
mc comment task_XXX "OpenClaw" "Read monitor_server.py (7.5KB). Found /api/agents and 
    /api/chats routes. Will add /api/executions for tool call visibility."

mc subtask task_XXX sub_002 done
mc comment task_XXX "OpenClaw" "Log format analyzed. Transcripts in 
    ~/.openclaw/transcripts/. Each entry has timestamp, tool name, args, result."

mc subtask task_XXX sub_003 done
mc comment task_XXX "OpenClaw" "New endpoint designed: /api/executions returns tool 
    calls with session key, tool name, args, timestamp, duration."

mc subtask task_XXX sub_004 done
mc comment task_XXX "OpenClaw" "SSE streaming implemented. Updates every 2 seconds 
    from tail -f on transcript files."

mc subtask task_XXX sub_005 done
mc comment task_XXX "OpenClaw" "Dashboard built. Shows live tool execution table 
    with filter by session."

mc subtask task_XXX sub_006 done
mc comment task_XXX "OpenClaw" "Tested with main session. Tool calls appearing in 
    real-time. Latency <500ms."

# 5. UPDATE subtasks when discovery happens
mc subtask task_XXX add "Step 7: Add tool execution filtering by type"
mc comment task_XXX "OpenClaw" "Discovered need for filtering during testing. 
    Adding subtask for filter feature."

# 6. Complete
mc comment task_XXX "OpenClaw" "All steps complete. Added filtering feature 
    discovered during testing. Deployed and verified."
mc status task_XXX review
```

**KEY POINTS:**
- **Research comes FIRST**: Understand the codebase before planning
- **Subtasks are SPECIFIC**: Based on actual files, functions, patterns found
- **Comments show DISCOVERY**: What you learned, what changed, what you found
- **UPDATE as you learn**: Add/modify subtasks when reality differs from plan
- **This is micromanagement by design - Anthony sees your thinking process.**

## Dashboard

**Mission Control Dashboard:** https://antonkonsta.github.io/mission-control-dashboard/

Anthony can click any task and see:
- Full description with all expectations
- Your step-by-step plan (subtasks)
- Your progress and current status (comments)
- When it was last updated

**If Anthony opens a task and can't understand the full picture = YOU FAILED**
