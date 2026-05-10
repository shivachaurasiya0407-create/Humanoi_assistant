#!/usr/bin/env python3
"""
Simple server runner - avoids encoding issues
"""
import sys
import os

# Fix encoding issues on Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Import and run
from api.server import start_server

if __name__ == "__main__":
    print("=" * 60)
    print("Starting Humanoid AI Assistant API Server")
    print("=" * 60)
    print("\n[SERVER] Starting on 0.0.0.0:5000")
    print("[SERVER] Frontend UI accessible at: http://localhost:5000")
    print("[SERVER] API endpoints available at: http://localhost:5000/api")
    print("[SERVER] WebSocket at: ws://localhost:5000/ws")
    print("\n[SERVER] Initializing...")
    
    try:
        start_server(host="0.0.0.0", port=5000)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)
