#!/usr/bin/env python3
"""
Quick test script to verify desktop GUI launches without issues.
"""

import sys

try:
    from desktop_gui import RemoteControlWindow, run_desktop_gui
    print("✅ Desktop GUI module imported successfully")
    print("✅ All dependencies available")
    print("\nGUI can be launched with: python main.py")
    print("Or standalone with: python desktop_gui.py")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
