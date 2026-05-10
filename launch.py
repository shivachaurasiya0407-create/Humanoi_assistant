#!/usr/bin/env python3
"""
Simple launcher script for the HUMAINOD AI System with Desktop GUI
"""

import os
import sys
import subprocess
import platform

def main():
    """Launch the system."""
    print("=" * 70)
    print("  HUMAINOD AI - System Launcher")
    print("=" * 70)
    print()
    print("🚀 Starting Humanoid AI Assistant with Desktop GUI...")
    print()
    
    # Get the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Run main.py
    try:
        # Default launch: GUI + API + AI OS
        cmd = [sys.executable, "main.py"]
        
        # On Windows, add --no-browser to prevent issues
        if platform.system() == "Windows":
            cmd.append("--no-browser")
        
        print(f"Running: {' '.join(cmd)}")
        print()
        
        result = subprocess.run(cmd)
        sys.exit(result.returncode)
        
    except KeyboardInterrupt:
        print("\n\n⏹️  System stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
