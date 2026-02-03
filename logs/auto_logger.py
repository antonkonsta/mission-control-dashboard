#!/usr/bin/env python3
"""
Auto-logging wrapper for agent tool calls
Intercepts tool calls and logs them to activity stream
"""

import sys
import json
from datetime import datetime, UTC
from pathlib import Path

sys.path.insert(0, '/root/.openclaw/workspace/logs')
from activity_logger import log_tool_call, log_decision, log_file_op, log_git

def log_from_transcript(transcript_path: str):
    """
    Parse OpenClaw session transcript and extract tool calls
    """
    if not Path(transcript_path).exists():
        return
    
    with open(transcript_path, 'r') as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                
                # Log tool calls
                if entry.get('role') == 'tool' and 'name' in entry:
                    tool_name = entry['name']
                    
                    # Parse parameters from content
                    params = {}
                    if 'content' in entry:
                        # Extract basic params (file paths, commands, etc.)
                        content = str(entry['content'])
                        if 'path' in content.lower():
                            # Try to extract path
                            pass
                    
                    log_tool_call(
                        tool=tool_name,
                        params=params,
                        result={"success": True}
                    )
                
            except:
                pass

def tail_and_log(transcript_path: str, interval: int = 5):
    """
    Tail transcript file and log new entries in real-time
    """
    import time
    
    last_position = 0
    
    while True:
        if Path(transcript_path).exists():
            with open(transcript_path, 'r') as f:
                f.seek(last_position)
                new_lines = f.readlines()
                last_position = f.tell()
                
                for line in new_lines:
                    try:
                        entry = json.loads(line.strip())
                        
                        if entry.get('role') == 'assistant':
                            # Log decisions from assistant messages
                            content = entry.get('content', '')
                            if 'decision' in content.lower() or 'starting' in content.lower():
                                log_decision(
                                    decision=content[:100],
                                    reason="From assistant message"
                                )
                    except:
                        pass
        
        time.sleep(interval)

if __name__ == "__main__":
    # Find latest session transcript
    sessions_dir = Path("/root/.openclaw/agents/main/sessions")
    if sessions_dir.exists():
        transcripts = sorted(sessions_dir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime)
        if transcripts:
            latest = transcripts[-1]
            print(f"Tailing {latest}")
            tail_and_log(str(latest))
