# HEARTBEAT.md - Proactive Work Loop

## 🚨 HEARTBEAT MESSAGE FORMAT
**When sending ANY message triggered by heartbeat, PREFIX it with:**
```
🔄 [HEARTBEAT]
```
This tells Anthony the message is automated, not a direct response to him.

Example: "🔄 [HEARTBEAT] Sub-agent task-naming-fix completed task_008."

## MONITORING DASHBOARDS (BURN THIS IN)
- **Mission Control:** https://antonkonsta.github.io/mission-control-dashboard/
  - Shows tasks.json - THIS IS WHERE ALL WORK MUST BE TRACKED
- **Task Monitor:** https://ubuntu-s-2vcpu-4gb-120gb-intel-atl1-01.tailb52a5a.ts.net/
  - Shows running sub-agents and activity in real-time
  - Anthony uses these to monitor everything you do

## CRITICAL RULE: MISSION CONTROL IS MANDATORY
**EVERYTHING Anthony asks you to do MUST be tracked in Mission Control.**
- **EVERYTHING = even small tasks, brief requests, "can you check X", "look into Y" - ALL OF IT**
- Create task FIRST using the `mc` CLI
- Git commit + push is AUTOMATIC via `mc` CLI
- THEN delegate to sub-agent or work on it
- NO EXCEPTIONS
- **If Anthony asks for something and you don't add it to Mission Control = FAILURE**
- **Anthony monitors via Mission Control dashboard - if it's not there, he can't see what you're doing**

### Mission Control CLI (`mc`) Commands
```bash
# Create a new task (auto-commits and pushes to dashboard)
mc create "Task title" "Description" priority

# Validate task exists before working (REQUIRED check)
mc validate task_XXX

# Show full task details
mc show task_XXX

# Update subtask status
mc subtask task_XXX sub_001 done

# Add a comment to a task
mc comment task_XXX "Author" "Comment text"

# Update task status
mc status task_XXX in_progress|review|done|backlog

# List all tasks
mc list [status]

# Manual sync (rarely needed - all commands auto-sync)
mc sync "message"
```

### Workflow (USE THE CLI)
1. **User makes request** → Run `mc create "title" "description" priority`
2. **Before working** → Run `mc validate task_XXX` (REQUIRED!)
3. **While working** → Run `mc subtask task_XXX sub_001 done` to update progress
4. **Add updates** → Run `mc comment task_XXX "OpenClaw" "Progress update"`
5. **Complete** → Run `mc status task_XXX done`

All `mc` commands automatically:
- Update `/root/.openclaw/workspace/data/tasks.json`
- Commit to git with `Mission Control:` prefix
- Push to `dashboard` remote (GitHub Pages)

### Manual Git Workflow (backup - prefer CLI)
If `mc` CLI is unavailable:
1. Modify `/root/.openclaw/workspace/data/tasks.json`
2. `cd /root/.openclaw/workspace`
3. `git add data/tasks.json`
4. `git commit -m "Mission Control: <description>"`
5. **`git push dashboard main`** ← REQUIRED FOR DASHBOARD UPDATE
6. Verify push succeeded before continuing work

**Two remotes:**
- `origin`: mission-control repo (optional)
- `dashboard`: antonkonsta/mission-control-dashboard (REQUIRED - this is what GitHub Pages uses)

### VALIDATION ENFORCEMENT
**BEFORE starting any work on a task:**
```bash
mc validate task_XXX
```
This returns:
- ✅ if task exists (shows title, status, progress)
- ❌ if task doesn't exist (blocks work, tells you to create it)

**If validation fails, DO NOT WORK ON IT. Create the task first.**

## MANDATORY ENFORCEMENT CHECKS (EVERY heartbeat - do these FIRST)

### 1. Memory Health Check
Check if memory logging is working properly.

### 2. Token Usage Check
Monitor context window usage.

### 3. Learning Log Check
Verify failures are being logged.

### 4. Sub-Agent Supervision (CRITICAL)
Check ALL running sub-agents:
- List sub-agent sessions
- **MATCH each sub-agent to its Mission Control task** (by label or sessionKey)
- Check last update time (if >2 min, demand status update from sub-agent)
- Review last message (if stuck/silent, prompt or kill+respawn)
- **Monitor until TRULY complete** - don't move to review until deliverable is done
- Update Mission Control task with sub-agent progress comments
- **ONLY move to 'review' when agent shows clear completion** (deliverable ready)
- Then ping Anthony
- Be STRICT - no excuses, demand results
- Kill and respawn failures immediately

### 5. ⚠️ MANDATORY SUB-AGENT NAMING RULE
**EVERY sub-agent MUST be spawned with a `label` parameter. NO EXCEPTIONS.**

When spawning a sub-agent via `sessions_spawn`:
```
label="task-name-here"  ← MANDATORY
```

**Good examples:**
- `label="doordash-research"` 
- `label="voice-fix"`
- `label="dashboard-upgrade"`
- `label="task-008-naming-fix"`

**Bad (FORBIDDEN):**
- Spawning without `label` parameter
- Using generic labels like `label="sub-agent"` or `label="task"`

**FAILURE CONDITIONS:**
- ❌ If Task Monitor shows **"⚠️ UNNAMED"** = YOU FAILED TO NAME IT
- ❌ If Task Monitor shows **"Unknown task"** = SESSION NOT MAPPED  
- ❌ Anthony sees unnamed agents = IMMEDIATE FAILURE

**Why this matters:**
- Anthony monitors via Task Monitor dashboard
- Unnamed agents are invisible/confusing
- Makes debugging and supervision impossible
- Shows lack of attention to detail

## ACTIVE WORK CHECK (After enforcement)

### Check Running Work
1. **Mission Control tasks in 'in_progress':**
   - Read `/root/.openclaw/workspace/data/tasks.json`
   - Find tasks with `"status": "in_progress"`
   - **JUDGE PROGRESS:** If all subtasks done OR deliverable complete → move to 'review' AUTOMATICALLY
   - Continue working on them, update subtasks, add comments
   - **NEVER wait for Anthony to tell you to move tasks to review**
   - Move to 'review' when complete, commit to git

## WORK QUEUE CHECK (Priority Order)

1. **Mission Control 'backlog' (high priority first):**
   - Read `/root/.openclaw/workspace/data/tasks.json`
   - Find tasks with `"status": "backlog"`
   - Sort by priority: high → medium → low
   - If found → move to 'in_progress', start working

## 🚨 CRITICAL: NEVER MOVE TASKS TO "DONE"

**ONLY ANTHONY CAN MARK TASKS AS DONE.**

- When you complete work → move to `review`
- NEVER move to `done` yourself
- Wait for Anthony's explicit approval
- This applies to ALL tasks, no exceptions

**Workflow:**
1. `backlog` → `in_progress` (you can do this)
2. `in_progress` → `review` (you can do this when work complete)
3. `review` → `done` (ONLY ANTHONY - NEVER YOU)

**If you move a task to "done" without Anthony's approval = IMMEDIATE FAILURE**

## EXECUTE OR REQUEST

- **If work found:** Start highest priority task, report what you're working on
- **If no work:** "No tasks queued. What should I work on next?"

## NEVER REPLY HEARTBEAT_OK IF THERE'S WORK

Only reply HEARTBEAT_OK if genuinely nothing to report.
