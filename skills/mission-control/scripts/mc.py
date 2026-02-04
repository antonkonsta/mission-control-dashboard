#!/usr/bin/env python3
"""
Mission Control CLI - Auto-sync tool for task management.
Ensures all tasks are tracked and synced to GitHub Pages dashboard.
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

TASKS_FILE = Path('/root/.openclaw/workspace/data/tasks.json')
WORKSPACE = Path('/root/.openclaw/workspace')


def load_tasks():
    """Load tasks from tasks.json"""
    with open(TASKS_FILE, 'r') as f:
        return json.load(f)


def save_tasks(data):
    """Save tasks and update lastUpdated timestamp"""
    data['lastUpdated'] = datetime.now(timezone.utc).isoformat()
    with open(TASKS_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def git_sync(message: str) -> bool:
    """Commit and push to dashboard remote"""
    try:
        # Stage tasks.json
        subprocess.run(
            ['git', 'add', 'data/tasks.json'],
            cwd=WORKSPACE,
            check=True,
            capture_output=True
        )
        
        # Commit
        subprocess.run(
            ['git', 'commit', '-m', f'Mission Control: {message}'],
            cwd=WORKSPACE,
            check=True,
            capture_output=True
        )
        
        # Push to dashboard remote (REQUIRED for GitHub Pages)
        result = subprocess.run(
            ['git', 'push', 'dashboard', 'main'],
            cwd=WORKSPACE,
            check=True,
            capture_output=True
        )
        
        print(f"✅ Synced to dashboard: {message}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git sync failed: {e.stderr.decode() if e.stderr else str(e)}")
        return False


def get_next_task_id(data) -> str:
    """Generate next task ID"""
    existing_ids = []
    for task in data['tasks']:
        if task['id'].startswith('task_'):
            try:
                existing_ids.append(int(task['id'].replace('task_', '')))
            except ValueError:
                pass
    next_num = max(existing_ids, default=0) + 1
    return f"task_{next_num:03d}"


def create_task(title: str, description: str = "", priority: str = "medium", subtasks: list = None) -> str:
    """Create a new task and sync to dashboard"""
    data = load_tasks()
    task_id = get_next_task_id(data)
    
    # Build subtasks with proper schema
    formatted_subtasks = []
    if subtasks:
        for i, st in enumerate(subtasks):
            if isinstance(st, str):
                formatted_subtasks.append({
                    "id": f"sub_{i+1:03d}",
                    "title": st,  # Use 'title' NOT 'text'
                    "done": False
                })
            elif isinstance(st, dict):
                formatted_subtasks.append({
                    "id": st.get('id', f"sub_{i+1:03d}"),
                    "title": st.get('title', st.get('text', '')),  # Handle both
                    "done": st.get('done', False)
                })
    
    task = {
        "id": task_id,
        "title": title,
        "description": description or title,
        "status": "in_progress",
        "priority": priority,
        "subtasks": formatted_subtasks,
        "comments": [],
        "createdAt": datetime.now(timezone.utc).isoformat()
    }
    
    data['tasks'].append(task)
    save_tasks(data)
    
    # Auto-sync to dashboard
    git_sync(f"Create {task_id}: {title[:50]}")
    
    print(f"✅ Created {task_id}: {title}")
    return task_id


def add_comment(task_id: str, author: str, text: str):
    """Add comment to a task and sync"""
    data = load_tasks()
    found = False
    
    for task in data['tasks']:
        if task['id'] == task_id:
            task['comments'].append({
                "author": author,
                "text": text,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            found = True
            break
    
    if not found:
        print(f"❌ Task {task_id} not found")
        return
    
    save_tasks(data)
    git_sync(f"Comment on {task_id}")
    print(f"✅ Added comment to {task_id}")


def update_subtask(task_id: str, subtask_id: str, done: bool = True):
    """Update subtask status and sync"""
    data = load_tasks()
    
    for task in data['tasks']:
        if task['id'] == task_id:
            for subtask in task['subtasks']:
                if subtask['id'] == subtask_id:
                    subtask['done'] = done
                    save_tasks(data)
                    git_sync(f"{task_id}/{subtask_id} {'done' if done else 'reopened'}")
                    print(f"✅ Updated {subtask_id}")
                    return
    
    print(f"❌ Subtask {subtask_id} not found in {task_id}")


def update_status(task_id: str, status: str):
    """Update task status and sync"""
    valid_statuses = ['backlog', 'in_progress', 'review', 'done']
    if status not in valid_statuses:
        print(f"❌ Invalid status. Use: {valid_statuses}")
        return
    
    data = load_tasks()
    
    for task in data['tasks']:
        if task['id'] == task_id:
            task['status'] = status
            save_tasks(data)
            git_sync(f"{task_id} → {status}")
            print(f"✅ {task_id} status → {status}")
            return
    
    print(f"❌ Task {task_id} not found")


def list_tasks(status_filter: str = None):
    """List all tasks, optionally filtered by status"""
    data = load_tasks()
    
    for task in data['tasks']:
        if status_filter and task['status'] != status_filter:
            continue
        
        status_emoji = {
            'backlog': '📋',
            'in_progress': '🔄',
            'review': '👀',
            'done': '✅'
        }.get(task['status'], '❓')
        
        priority_emoji = {
            'critical': '🔴',
            'high': '🟠',
            'medium': '🟡',
            'low': '🟢'
        }.get(task.get('priority', 'medium'), '⚪')
        
        done_subtasks = sum(1 for st in task.get('subtasks', []) if st.get('done'))
        total_subtasks = len(task.get('subtasks', []))
        
        print(f"{status_emoji} {priority_emoji} {task['id']}: {task['title']}")
        if total_subtasks > 0:
            print(f"   └─ Subtasks: {done_subtasks}/{total_subtasks}")


def main():
    if len(sys.argv) < 2:
        print("Mission Control CLI")
        print("Usage:")
        print("  mc.py create <title> [description] [priority]")
        print("  mc.py comment <task_id> <author> <text>")
        print("  mc.py subtask <task_id> <subtask_id> [done|undone]")
        print("  mc.py status <task_id> <status>")
        print("  mc.py list [status]")
        print("  mc.py sync <message>")
        return
    
    cmd = sys.argv[1]
    
    if cmd == 'create':
        title = sys.argv[2] if len(sys.argv) > 2 else "Untitled task"
        desc = sys.argv[3] if len(sys.argv) > 3 else ""
        priority = sys.argv[4] if len(sys.argv) > 4 else "medium"
        create_task(title, desc, priority)
    
    elif cmd == 'comment':
        if len(sys.argv) < 5:
            print("Usage: mc.py comment <task_id> <author> <text>")
            return
        add_comment(sys.argv[2], sys.argv[3], sys.argv[4])
    
    elif cmd == 'subtask':
        if len(sys.argv) < 4:
            print("Usage: mc.py subtask <task_id> <subtask_id> [done|undone]")
            return
        done = sys.argv[4] != 'undone' if len(sys.argv) > 4 else True
        update_subtask(sys.argv[2], sys.argv[3], done)
    
    elif cmd == 'status':
        if len(sys.argv) < 4:
            print("Usage: mc.py status <task_id> <status>")
            return
        update_status(sys.argv[2], sys.argv[3])
    
    elif cmd == 'list':
        status_filter = sys.argv[2] if len(sys.argv) > 2 else None
        list_tasks(status_filter)
    
    elif cmd == 'sync':
        message = sys.argv[2] if len(sys.argv) > 2 else "Manual sync"
        git_sync(message)
    
    else:
        print(f"Unknown command: {cmd}")


if __name__ == '__main__':
    main()
