#!/usr/bin/env python3
"""
Main Startup Controller for Humanoid AI System with Sync.
"""

import threading
import sys
import os
import asyncio
import time

async def initialize_sync():
    """Initialize sync on startup."""
    try:
        from sync import get_sync_manager
        manager = get_sync_manager()
        await manager.connect_mongo()
        await manager.pull_startup()
        print("[SYNC] Initialized - Ready for multi-device")
    except Exception as e:
        print(f"[SYNC] Skipped (Docker Redis/Mongo): {e}")

def start_backend():
    """Start FastAPI + WebSocket."""
    from api.server import start_server
    try:
        start_server(host="0.0.0.0", port=8000)
    except Exception as e:
        print(f"[ERROR] Server failed: {e}")
        sys.exit(1)

def initialize_ai():
    """Background AI init."""
    from main import initialize_application
    print("[AI] Initializing...")
    try:
        chat_engine = initialize_application()
        print("[AI] Ready" if chat_engine else "[AI] Failed - Check keys")
    except Exception as e:
        print(f"[AI] Error: {e}")

def print_instructions():
    """Startup instructions."""
    print("\n" + "="*70)
    print("🚀 HUMANOID AI SYSTEM w/ SYNC READY 🚀")
    print("="*70)
    print("🌐 Backend: http://localhost:8000")
    print("🔌 WebSocket: ws://localhost:8000/ws")
    print("\n📱 Frontend: cd frontend && npm run dev")
    print("📊 Sync Status: Check TODO.md")
    print("="*70)

if __name__ == "__main__":
    try:
        import uvicorn, fastapi
    except ImportError:
        print("[ERROR] pip install fastapi uvicorn")
        sys.exit(1)

    print_instructions()
    
    # Background sync + AI init
    asyncio.run(initialize_sync())
    threading.Thread(target=initialize_ai, daemon=True).start()
    
    try:
        start_backend()
    except KeyboardInterrupt:
        print("\n[SYSTEM] Shutdown...")
        sys.exit(0)

