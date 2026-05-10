@echo off
echo ==========================================
echo   HUMAINOD AI OS - DEPENDENCY INSTALLER
echo ==========================================
echo.
echo [1/3] Updating pip...
python -m pip install --upgrade pip

echo.
echo [2/3] Installing Core Dependencies...
pip install -r requirements.txt

echo.
echo [3/3] Installing Torch (GPU optimized if possible)...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

echo.
echo [DONE] All dependencies should be installed now.
echo Try running 'python main.py' again.
pause
