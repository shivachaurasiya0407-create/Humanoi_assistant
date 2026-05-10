@echo off
REM Updated Windows Installation Script for Humanoid AI Assistant
REM Handles Gemini API, voice deps (pyttsx3, sounddevice, vosk), optional TTS

echo ============================================
echo  Humanoid AI Assistant - Windows Installer v2.0
echo ============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3.10+ not found.
    echo Install from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [INFO] Python OK:
python --version
echo.

REM Python version for TTS compatibility
for /f "tokens=2" %%i in ('python -c "import sys; print(sys.version)"') do set PYTHON_VER=%%i
echo [INFO] Python %PYTHON_VER%

REM Create .venv if not exist
if not exist ".venv" (
    echo [INFO] Creating .venv...
    python -m venv .venv
)

echo [INFO] Activating .venv...
call .venv\Scripts\activate.bat

echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

echo [INFO] Installing from requirements.txt (pyttsx3 voice, Vosk STT, sounddevice mic)...
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Core install failed.
    pause
    exit /b 1
)

echo [SUCCESS] Core deps installed! (TTS commented for Python 3.12+, see requirements-tts.txt)

echo.
echo ============================================
echo  Voice Setup Notes
echo ============================================
echo.
echo STT (voice to text): Vosk + sounddevice - models ready
echo TTS (text to voice): pyttsx3 - offline
echo.
echo Windows TTS Voices: Settings ^> Time ^& Language ^> Speech ^> Manage voices ^> Add voices
echo Mic Privacy: Settings ^> Privacy ^> Microphone ^> Allow desktop apps
echo.
echo For Coqui TTS (neural voices): Python 3.11 venv + requirements-tts.txt
echo.
echo ============================================
echo  Next Steps
echo ============================================
echo 1. .env - Add GOOGLE_GEMINI_API_KEY (https://aistudio.google.com/app/apikey)
echo 2. python main.py ^<or^> .venv\Scripts\python main.py
echo 3. /voice for voice mode
echo.
pause


echo [WARNING] pipwin method failed. Trying Method 2...

REM Try Method 2: Direct pip install (works if build tools are installed)
echo [INFO] Attempting Method 2: Direct pip install...
pip install pyaudio

if not errorlevel 1 (
    echo [SUCCESS] PyAudio installed successfully via pip!
    goto install_complete
)

echo [WARNING] Direct pip install failed.
echo.
echo ============================================
echo  PyAudio Installation Failed
echo ============================================
echo.
echo Please try one of these alternatives:
echo.
echo 1. Install Microsoft Visual C++ Build Tools:
echo    https://visualstudio.microsoft.com/visual-cpp-build-tools/
echo    - Install "Desktop development with C++" workload
echo    - Restart your computer
echo    - Run this script again
echo.
echo 2. Download a pre-built wheel from:
echo    https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
echo    Then install with: pip install path\to\PyAudio-*.whl
echo.
echo 3. Use the application without voice input:
echo    The chat application will work normally without PyAudio.
echo    Voice input features will be unavailable.
echo.

pause
exit /b 1

:install_complete
echo.
echo ============================================
echo  Installation Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Copy .env.example to .env and add your OpenAI API key
echo 2. Download a Vosk model (see README.md)
echo 3. Run: python main.py
echo.
echo For voice input, type /voice in the chat.
echo.
pause