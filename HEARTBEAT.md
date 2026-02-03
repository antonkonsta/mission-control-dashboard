# HEARTBEAT.md - Proactive Work Loop

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
- Check last update time (if >2 min, demand status)
- Review last message (if stuck/silent, prompt or kill+respawn)
- Report progress to Anthony
- Be STRICT - no excuses, demand results
- Kill and respawn failures immediately

## ACTIVE WORK CHECK (After enforcement)

### Check Running Work
1. **Mission Control tasks in 'in_progress':**
   - Read `/root/.openclaw/workspace/data/tasks.json`
   - Find tasks with `"status": "in_progress"`
   - Continue working on them, update subtasks, add comments
   - Move to 'review' when complete

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
