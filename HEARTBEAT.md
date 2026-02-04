# HEARTBEAT.md - Proactive Work Loop

## MONITORING DASHBOARDS (BURN THIS IN)
- **Mission Control:** https://antonkonsta.github.io/mission-control-dashboard/
  - Shows tasks.json - THIS IS WHERE ALL WORK MUST BE TRACKED
- **Task Monitor:** https://ubuntu-s-2vcpu-4gb-120gb-intel-atl1-01.tailb52a5a.ts.net/
  - Shows running sub-agents and activity in real-time
  - Anthony uses these to monitor everything you do

## CRITICAL RULE: MISSION CONTROL IS MANDATORY
**EVERYTHING Anthony asks you to do MUST be tracked in Mission Control.**
- **EVERYTHING = even small tasks, brief requests, "can you check X", "look into Y" - ALL OF IT**
- Create task in `/root/.openclaw/workspace/data/tasks.json` FIRST
- Commit to git IMMEDIATELY
- THEN delegate to sub-agent or work on it
- NO EXCEPTIONS
- **If Anthony asks for something and you don't add it to Mission Control = FAILURE**
- **Anthony monitors via Mission Control dashboard - if it's not there, he can't see what you're doing**

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
- **EVERY sub-agent MUST be spawned with label=<task-name>** (e.g., "doordash-research", "voice-fix")
- **If you see "Unknown task" in Task Monitor = YOU FAILED TO NAME IT**
- Check last update time (if >2 min, demand status update from sub-agent)
- Review last message (if stuck/silent, prompt or kill+respawn)
- **Monitor until TRULY complete** - don't move to review until deliverable is done
- Update Mission Control task with sub-agent progress comments
- **ONLY move to 'review' when agent shows clear completion** (deliverable ready)
- Then ping Anthony
- Be STRICT - no excuses, demand results
- Kill and respawn failures immediately

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

## EXECUTE OR REQUEST

- **If work found:** Start highest priority task, report what you're working on
- **If no work:** "No tasks queued. What should I work on next?"

## NEVER REPLY HEARTBEAT_OK IF THERE'S WORK

Only reply HEARTBEAT_OK if genuinely nothing to report.
