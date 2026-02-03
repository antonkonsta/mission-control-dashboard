#!/usr/bin/env python3
"""
Activity Logger - Captures all agent actions for real-time monitoring dashboard

Logs to JSONL file that can be streamed to live dashboard.
"""

import json
import os
from datetime import datetime, UTC
from pathlib import Path
from typing import Optional, Dict, Any

LOG_DIR = Path("/root/.openclaw/workspace/logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
ACTIVITY_LOG = LOG_DIR / "activity-stream.jsonl"

# Rotation: keep last 1000 entries
MAX_ENTRIES = 1000

def log_activity(
    activity_type: str,
    data: Dict[str, Any],
    context: Optional[Dict[str, Any]] = None
):
    """
    Log an activity event to the stream.
    
    Args:
        activity_type: Type of activity (tool_call, decision, file_op, git, error)
        data: Activity-specific data
        context: Optional context (task_id, subtask_id, etc.)
    """
    entry = {
        "timestamp": datetime.now(UTC).isoformat(),
        "type": activity_type,
        "data": data
    }
    
    if context:
        entry["context"] = context
    
    # Append to log file
    with open(ACTIVITY_LOG, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    
    # Rotate if needed
    _rotate_if_needed()

def _rotate_if_needed():
    """Keep only last MAX_ENTRIES in log file"""
    if not ACTIVITY_LOG.exists():
        return
    
    with open(ACTIVITY_LOG, 'r') as f:
        lines = f.readlines()
    
    if len(lines) > MAX_ENTRIES:
        with open(ACTIVITY_LOG, 'w') as f:
            f.writelines(lines[-MAX_ENTRIES:])

def log_tool_call(tool: str, params: Dict[str, Any], result: Optional[Dict[str, Any]] = None, context: Optional[Dict[str, Any]] = None):
    """Log a tool call (read, write, exec, web_search, etc.)"""
    log_activity("tool_call", {
        "tool": tool,
        "params": params,
        "result": result
    }, context)

def log_decision(decision: str, reason: str, context: Optional[Dict[str, Any]] = None):
    """Log a decision point"""
    log_activity("decision", {
        "decision": decision,
        "reason": reason
    }, context)

def log_file_op(operation: str, path: str, size: Optional[int] = None, context: Optional[Dict[str, Any]] = None):
    """Log a file operation (read, write, edit, delete)"""
    log_activity("file_op", {
        "operation": operation,
        "path": path,
        "size": size
    }, context)

def log_git(action: str, message: str, files: Optional[list] = None, context: Optional[Dict[str, Any]] = None):
    """Log a git operation (commit, push, pull)"""
    log_activity("git", {
        "action": action,
        "message": message,
        "files": files
    }, context)

def log_error(error: str, details: Optional[str] = None, context: Optional[Dict[str, Any]] = None):
    """Log an error"""
    log_activity("error", {
        "error": error,
        "details": details
    }, context)

def get_recent_activity(limit: int = 100) -> list:
    """Get recent activity entries"""
    if not ACTIVITY_LOG.exists():
        return []
    
    with open(ACTIVITY_LOG, 'r') as f:
        lines = f.readlines()
    
    entries = []
    for line in lines[-limit:]:
        try:
            entries.append(json.loads(line.strip()))
        except:
            pass
    
    return entries

# Example usage (for testing)
if __name__ == "__main__":
    # Test logging
    log_decision(
        decision="Start monitoring system task",
        reason="Highest priority in backlog",
        context={"task_id": "task_004"}
    )
    
    log_tool_call(
        tool="read",
        params={"path": "/root/.openclaw/workspace/data/tasks.json"},
        result={"success": True, "size": 12345},
        context={"task_id": "task_004", "subtask_id": "sub_003"}
    )
    
    log_file_op(
        operation="write",
        path="/root/.openclaw/workspace/logs/activity_logger.py",
        size=3456,
        context={"task_id": "task_004"}
    )
    
    log_git(
        action="commit",
        message="Add activity logger",
        files=["logs/activity_logger.py"],
        context={"task_id": "task_004"}
    )
    
    # Show recent activity
    print("Recent activity:")
    for entry in get_recent_activity(limit=5):
        print(json.dumps(entry, indent=2))
