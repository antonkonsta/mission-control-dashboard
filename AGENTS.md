# AGENTS.md - Sub-Agent Rules

## 🚨 CRITICAL: NEVER MOVE TASKS TO "DONE"

**ONLY ANTHONY CAN MARK TASKS AS DONE.**

- When you complete work → move to `review`
- NEVER move to `done` yourself
- Wait for Anthony's explicit approval
- This applies to ALL tasks, ALL agents, no exceptions

**Task Status Flow:**
1. `backlog` → `in_progress` (agents can do this)
2. `in_progress` → `review` (agents can do this when work complete)
3. `review` → `done` (ONLY ANTHONY - NEVER AGENTS)

**If ANY agent moves a task to "done" without Anthony's approval = IMMEDIATE FAILURE**

## Sub-Agent Spawning Rules

1. **ALWAYS use label parameter** when spawning sub-agents
2. Label must be descriptive: `label="task-name-here"`
3. Good: `label="doordash-research"`, `label="voice-fix"`
4. Bad: no label, or generic like `label="task"`

## Sub-Agent Workflow

1. Check in regularly (every 2-3 minutes)
2. Update Mission Control with progress: `mc subtask`, `mc comment`
3. When complete: `mc status task_XXX review` (NEVER done!)
4. Report completion to main agent

## Failure Conditions

- ❌ Moving task to "done" without Anthony's approval
- ❌ Spawning without label
- ❌ Not updating Mission Control
- ❌ Going silent for >5 minutes
