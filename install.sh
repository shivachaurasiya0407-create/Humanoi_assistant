#!/bin/bash
# Installation Script for Humanoid AI Assistant (Linux/macOS)
# This script installs all dependencies including PyAudio

echo "============================================"
echo " Humanoid AI Assistant - Installer"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed."
    echo "Please install Python 3.10+ first."
    exit 1
fi

echo "[INFO] Python found:"
python3 --version
echo ""

# Detect OS
OS="$(uname -s)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "[INFO] Creating virtual environment..."
    python3 -m venv venv
fi

echo "[INFO] Activating virtual environment..."
source venv/bin/activate

echo "[INFO] Upgrading pip..."
pip install --upgrade pip

echo ""
echo "============================================"
echo " Installing Core Dependencies"
echo "============================================"
echo ""

echo "[INFO] Installing OpenAI SDK and python-dotenv..."
pip install openai python-dotenv

echo ""
echo "============================================"
echo " Installing Vosk (Speech Recognition)"
echo "============================================"
echo ""

echo "[INFO] Installing Vosk..."
pip install vosk

echo ""
echo "[INFO] Vosk installed. Remember to download a Vosk model separately!"
echo "       See README.md for instructions."
echo ""

echo "============================================"
echo " Installing PyAudio (Microphone Input)"
echo "============================================"
echo ""

case "$OS" in
    Linux)
        # Check for common Linux distributions
        if [ -f "/etc/debian_version" ] || [ -f "/etc/ubuntu_version" ] || grep -q "Ubuntu" /etc/os-release 2>/dev/null; then
            echo "[INFO] Ubuntu/Debian detected. Installing system dependencies..."
            sudo apt-get update
            sudo apt-get install -y python3-pyaudio portaudio19-dev
            
        elif [ -f "/etc/arch-release" ]; then
            echo "[INFO] Arch Linux detected. Installing system dependencies..."
            sudo pacman -S --noconfirm python-pyaudio portaudio
            
        elif [ -f "/etc/fedora-release" ] || [ -f "/etc/redhat-release" ]; then
            echo "[INFO] Fedora/RedHat detected. Installing system dependencies..."
            sudo dnf install -y portaudio-devel python3-pyaudio
            
        elif [ -f "/etc/almalinux-release" ] || [ -f "/etc/rocky-release" ]; then
            echo "[INFO] AlmaLinux/Rocky Linux detected. Installing system dependencies..."
            sudo dnf install -y portaudio-devel python3-pyaudio
            
        else
            echo "[INFO] Installing PyAudio via pip (system dependencies may be required)..."
            echo "       If this fails, install portaudio development files first."
        fi
        ;;
        
    Darwin)
        echo "[INFO] macOS detected. Installing PortAudio..."
        if command -v brew &> /dev/null; then
            brew install portaudio
        else
            echo "[WARNING] Homebrew not found. Please install PortAudio manually:"
            echo "          1. Install Homebrew: https://brew.sh"
            echo "          2. Run: brew install portaudio"
            exit 1
        fi
        ;;
        
    *)
        echo "[WARNING] Unknown OS: $OS"
        echo "          Please install PortAudio development files manually."
        ;;
esac

# Install PyAudio via pip
echo "[INFO] Installing PyAudio via pip..."
pip install pyaudio

if [ $? -eq 0 ]; then
    echo "[SUCCESS] PyAudio installed successfully!"
else
    echo ""
    echo "============================================"
    echo " PyAudio Installation Failed"
    echo "============================================"
    echo ""
    echo "Please install PortAudio development files first:"
    echo ""
    echo "Ubuntu/Debian:"
    echo "  sudo apt-get install portaudio19-dev python3-pyaudio"
    echo ""
    echo "Arch Linux:"
    echo "  sudo pacman -S portaudio python-pyaudio"
    echo ""
    echo "Fedora/RedHat:"
    echo "  sudo dnf install portaudio-devel python3-pyaudio"
    echo ""
    echo "macOS:"
    echo "  brew install portaudio"
    echo ""
    echo "Then run this script again."
    echo ""
    echo "Alternatively, the chat application will work without voice input."
    exit 1
fi

echo ""
echo "============================================"
echo " Installation Complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env and add your OpenAI API key"
echo "2. Download a Vosk model (see README.md)"
echo "3. Run: python main.py"
echo ""
echo "For voice input, type /voice in the chat."
echo ""