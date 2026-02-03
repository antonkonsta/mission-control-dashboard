#!/usr/bin/env python3
"""
Todoist CLI wrapper - uses API token from environment
"""
import os
import sys
from todoist_api_python.api import TodoistAPI

def main():
    token = os.environ.get('TODOIST_API_TOKEN')
    if not token:
        print("Error: TODOIST_API_TOKEN not set")
        sys.exit(1)
    
    api = TodoistAPI(token)
    
    # Simple list command
    if len(sys.argv) == 1 or sys.argv[1] in ['list', 'today']:
        try:
            count = 0
            total = 0
            for page in api.get_tasks():
                for task in page:
                    total += 1
                    if count < 20:
                        due_str = "No due"
                        if hasattr(task, 'due') and task.due:
                            due_str = task.due.date if hasattr(task.due, 'date') else str(task.due)
                        print(f"• {task.content} (Due: {due_str})")
                        count += 1
                    
            print(f"\nTotal: {total} tasks")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        print(f"Command '{sys.argv[1]}' not implemented yet")
        print("Supported: list, today")
        sys.exit(1)

if __name__ == '__main__':
    main()
