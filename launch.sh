#!/bin/bash

# HUMAINOD AI - Desktop Launcher for Linux/Mac
# Run this file to start the complete AI system with Desktop GUI

echo ""
echo "========================================================================"
echo ""
echo "  HUMAINOD AI - Humanoid Assistant with Desktop GUI"
echo ""
echo "  Starting system... (Desktop GUI will launch automatically)"
echo ""
echo "========================================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

# Run the main system
python3 main.py --no-browser
