#!/usr/bin/env python3
"""
Activity Monitor - Flask backend with Server-Sent Events

Serves live dashboard and streams activity updates in real-time.
"""

from flask import Flask, render_template, Response, jsonify
import json
import time
from pathlib import Path
import sys

# Add logs directory to path for activity_logger
sys.path.insert(0, str(Path(__file__).parent))
from activity_logger import get_recent_activity, ACTIVITY_LOG

app = Flask(__name__)

@app.route('/')
def dashboard():
    """Serve the dashboard HTML"""
    return render_template('dashboard.html')

@app.route('/api/history')
def history():
    """Get recent activity history"""
    limit = int(request.args.get('limit', 100))
    return jsonify(get_recent_activity(limit=limit))

@app.route('/api/stream')
def stream():
    """Server-Sent Events stream for live updates"""
    def generate():
        last_position = 0
        
        while True:
            # Read new entries since last position
            if ACTIVITY_LOG.exists():
                with open(ACTIVITY_LOG, 'r') as f:
                    lines = f.readlines()
                
                if len(lines) > last_position:
                    # Send new entries
                    for line in lines[last_position:]:
                        try:
                            entry = json.loads(line.strip())
                            yield f"data: {json.dumps(entry)}\\n\\n"
                        except:
                            pass
                    
                    last_position = len(lines)
            
            time.sleep(10)  # Update every 10 seconds as requested
    
    return Response(generate(), mimetype='text/event-stream')

@app.route('/api/tasks')
def tasks():
    """Get current Mission Control tasks"""
    tasks_file = Path('/root/.openclaw/workspace/data/tasks.json')
    if tasks_file.exists():
        with open(tasks_file, 'r') as f:
            return jsonify(json.load(f))
    return jsonify({"tasks": []})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=False, threaded=True)
