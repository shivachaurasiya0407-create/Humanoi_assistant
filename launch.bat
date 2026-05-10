@echo off
REM
REM HUMAINOD AI - Desktop Launcher for Windows
REM Run this file to start the complete AI system with Desktop GUI
REM

echo.
echo ========================================================================
echo.
echo   HUMAINOD AI - Humanoid Assistant with Desktop GUI
echo.
echo   Starting system... (Desktop GUI will launch automatically)
echo.
echo ========================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

REM Run the main system
python main.py --no-browser

pause
