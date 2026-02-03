#!/usr/bin/env python3
"""
Simple voice response handler
Reads transcription, sends to isolated session, returns response
"""

import sys
import json
import subprocess
import os

def main():
    # Read transcription from stdin (passed by gateway)
    try:
        data = json.loads(sys.stdin.read())
        transcript = data.get("transcribed", "")
        
        if not transcript:
            print(json.dumps({"error": "No transcription"}))
            sys.exit(1)
        
        # Use openclaw CLI to send to isolated session and get response
        # This prevents context pollution in main session
        result = subprocess.run(
            [
                "openclaw", "message", "send",
                "--session", "voice-isolated",
                "--message", transcript,
                "--wait-reply"
            ],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            # Got response - send it back
            response_text = result.stdout.strip()
            print(json.dumps({
                "transcribed": transcript,
                "response": response_text
            }))
        else:
            # Failed to get response
            print(json.dumps({
                "transcribed": transcript,
                "error": "Failed to generate response"
            }))
            sys.exit(1)
            
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

if __name__ == "__main__":
    main()
