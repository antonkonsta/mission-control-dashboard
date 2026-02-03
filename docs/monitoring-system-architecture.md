# Real-Time Activity Monitoring System - Architecture Design

## Requirements
- **Detail level:** EVERYTHING (every tool call, file read, decision)
- **Interface:** Live web dashboard
- **Update frequency:** Every 10 seconds
- **Priority:** HIGHEST

## Architecture Overview

### 1. Activity Logging Layer
**What to capture:**
- Every tool call (read, write, exec, web_search, etc.)
- Tool parameters (file paths, commands, URLs)
- Tool results (success/failure, output size)
- Decision points (which task selected, priority changes)
- File operations (reads, writes, edits)
- Git commits (what changed, why)
- Session state (tokens used, current task, subtask progress)

**Implementation:**
- Wrapper around OpenClaw tool calls
- Log to structured JSON stream
- File: `/root/.openclaw/workspace/logs/activity-stream.jsonl`
- Format: `{"timestamp": "ISO8601", "type": "tool_call|decision|file_op|git", "data": {...}}`

### 2. Dashboard Backend
**Technology:** Simple HTTP server (Python + Flask or Node.js)
- Serve static HTML dashboard
- WebSocket or Server-Sent Events (SSE) for live updates
- Read activity-stream.jsonl and stream to clients
- Endpoint: `http://localhost:3000` (or Tailscale Funnel)

**API Endpoints:**
- `GET /` → Dashboard HTML
- `GET /stream` → SSE endpoint for live activity
- `GET /history?limit=100` → Recent activity (for initial load)
- `GET /tasks` → Current Mission Control tasks JSON

### 3. Dashboard Frontend
**Technology:** Simple HTML + JavaScript (no framework overhead)
- Auto-refreshing activity feed
- Real-time updates via SSE (every 10 seconds or instant)
- Color-coded activity types:
  - 🔧 Tool calls (blue)
  - 📁 File operations (green)
  - 🔀 Git commits (purple)
  - 🎯 Decisions (orange)
  - ⚠️ Errors (red)

**Layout:**
```
┌─────────────────────────────────────────────┐
│  OpenClaw Activity Monitor                  │
│  Current Task: [task name]                  │
│  Tokens: 116,584 / 128,000 (91.1%)          │
│  Uptime: 2h 15m                             │
├─────────────────────────────────────────────┤
│  Live Activity Feed (auto-scroll)           │
│  ┌─────────────────────────────────────┐   │
│  │ 17:59:45 🔧 exec: python3 ...       │   │
│  │ 17:59:46 📁 read: tasks.json        │   │
│  │ 17:59:47 🎯 Decision: Start task 4  │   │
│  │ 17:59:48 🔀 git commit: "..."       │   │
│  │ [continues...]                       │   │
│  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

### 4. Integration Points

**A. Heartbeat Integration**
- Heartbeat logs activity: "Running enforcement checks"
- Logs task transitions: "Switched from task_003 to task_004"
- Logs decisions: "Picked highest priority task"

**B. Tool Call Wrapper**
- Intercept every tool call before execution
- Log parameters + result
- No performance impact (async logging)

**C. Mission Control Integration**
- Read tasks.json every 10 seconds
- Show current task progress in header
- Link to Mission Control dashboard

## Implementation Plan

### Phase 1: Logging (30 minutes)
1. Create activity logger module
2. Add wrapper for tool calls
3. Test logging to JSONL file
4. Verify log rotation (keep last 1000 entries)

### Phase 2: Backend Server (45 minutes)
1. Simple Flask server with SSE
2. Serve dashboard HTML
3. Stream activity from JSONL
4. Test with curl

### Phase 3: Dashboard UI (60 minutes)
1. HTML + CSS for layout
2. JavaScript SSE client
3. Auto-scroll activity feed
4. Color-coded entries
5. Token usage in header

### Phase 4: Deploy & Test (15 minutes)
1. Start server on boot (systemd service)
2. Configure Tailscale Funnel (public URL)
3. Test with real heartbeat activity
4. Verify 10-second updates

## Technical Details

### Activity Log Entry Format
```json
{
  "timestamp": "2026-02-03T22:59:45.123Z",
  "type": "tool_call",
  "tool": "exec",
  "params": {
    "command": "python3 /tmp/script.py"
  },
  "result": {
    "success": true,
    "output": "✓ Task completed"
  },
  "context": {
    "task_id": "task_004",
    "subtask_id": "sub_002"
  }
}
```

### SSE Stream Format
```
data: {"timestamp": "...", "type": "tool_call", ...}

data: {"timestamp": "...", "type": "decision", ...}

```

### Deployment
- Server runs on port 3000
- Tailscale Funnel: `openclaw.tail-scale.ts.net` (or similar)
- Systemd service: `openclaw-monitor.service`
- Auto-start on boot

## Security
- No authentication for now (trusted network via Tailscale)
- Future: Add basic auth or token-based access
- Activity logs may contain sensitive data (file paths, commands)

## Performance
- Log file size: ~1 MB per day (estimated)
- Rotation: Keep last 1000 entries (~100 KB)
- SSE overhead: Negligible (<1% CPU)
- Dashboard refresh: Every 10 seconds (as requested)

## Alternative: Simpler Approach
If full dashboard is too complex, fallback to:
- Log activity to file
- Tail -f in browser via simple HTTP endpoint
- Plain text stream (no fancy UI)

**Recommendation:** Build full dashboard (better UX, worth the effort)

---

**Next Steps:**
1. Start with logging layer (Phase 1)
2. Test activity capture
3. Build backend server (Phase 2)
4. Create dashboard UI (Phase 3)
5. Deploy and verify with Anthony

**Time estimate:** 2.5 hours total
