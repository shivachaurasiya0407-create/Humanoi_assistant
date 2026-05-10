# 🖥️ Desktop GUI Integration - Complete Guide

## ✨ What's New

The Humanoid AI Assistant now includes a **production-grade PyQt5 Desktop GUI** that automatically launches when you run the system. It provides real-time monitoring, system metrics, and complete remote control capabilities.

---

## 🚀 Quick Start (3 Steps)

### Step 1: Ensure Dependencies Are Installed
```bash
pip install -r requirements.txt
```

### Step 2: Run the System
Choose one of these:

**Windows:**
```bash
launch.bat
```

**Linux/Mac:**
```bash
bash launch.sh
```

**Any System:**
```bash
python main.py
```

### Step 3: See the Desktop GUI Launch!
- ✅ Desktop window opens automatically
- ✅ Live system metrics displayed
- ✅ WebSocket connection to backend
- ✅ API server running on port 5000
- ✅ React web frontend available

---

## 🎨 Desktop GUI Features

### Live System Monitoring
```
┌─────────────────────────────────────────────────────────┐
│  HUMAINOD AI - v2.0 OS              11:45:32 PM         │
├─────────────────────────────────────────────────────────┤
│  CPU: 23% │ RAM: 48% │ GPU: 37% │ Disk: 62%           │
│  Network: 128 Mbps                                      │
└─────────────────────────────────────────────────────────┘
```

### Main Panels

| Panel | Feature |
|-------|---------|
| **System Status** | Module health & connection status |
| **System Metrics** | Real-time CPU, RAM, GPU, Disk, Network |
| **AI Core** | Neural engine visualization & intensity |
| **Vision System** | Live screen analysis & object detection |
| **Commands Panel** | Remote command history with status |
| **Automation Engine** | Current task progress & steps |
| **Memory & Context** | Knowledge base stats & learning progress |
| **Voice System** | Listening toggle & audio controls |
| **Live Logs** | System events & AI responses |

---

## 🏗️ Architecture

### Process Layout
```
main.py (Entry Point)
├── AI OS Core (Backend Processing)
│   ├── Agent Controller
│   ├── Chat Engine
│   ├── Learning Engine
│   └── Task Router
│
├── API Server (port 5000)
│   ├── REST endpoints
│   ├── WebSocket server
│   └── Static file serving
│
├── Desktop GUI (Separate Thread)
│   ├── PyQt5 Window
│   ├── System Metrics Polling
│   ├── WebSocket Client
│   └── Live Updates Display
│
└── React Frontend (Optional)
    ├── Vite Dev Server
    ├── React 19 Components
    ├── WebSocket Integration
    └── Three.js Visualization
```

### Data Flow
```
GUI Thread                Backend Thread              Frontend (Browser)
    │                          │                           │
    │◄──── System Metrics ────►│                           │
    │                          │◄──── WebSocket ───────────►│
    │                          │────── Live Data ──────────►│
    │◄──── Commands ──────────►│                           │
    │     (Execute)            │                           │
```

---

## 📋 Usage Modes

### Mode 1: Full System (Recommended)
```bash
python main.py
```
- ✅ Desktop GUI (auto-launches)
- ✅ API Server (port 5000)
- ✅ WebSocket (real-time updates)
- ✅ AI OS (all modules)
- ✅ Browser (optional, auto-opens)

**Best for:** Complete experience with all features

### Mode 2: GUI + Backend (No Browser)
```bash
python main.py --no-browser
```
- ✅ Desktop GUI (auto-launches)
- ✅ API Server (port 5000)
- ✅ WebSocket (real-time updates)
- ✅ AI OS (all modules)
- ❌ Browser (manual access: http://localhost:5000)

**Best for:** Desktop users who don't need web UI

### Mode 3: GUI Only
```bash
python desktop_gui.py
```
- ✅ Desktop GUI only
- ❌ API Server
- ❌ WebSocket (limited functionality)
- ❌ AI OS

**Best for:** Testing GUI in isolation

### Mode 4: CLI (Legacy)
```bash
python main.py --cli
```
- ✅ Terminal interface
- ✅ API Server
- ✅ AI OS
- ❌ Desktop GUI
- ❌ React Frontend

**Best for:** Server environments, scripting

### Mode 5: Headless (Backend Only)
```bash
python main.py --headless --no-browser
```
- ✅ API Server
- ✅ WebSocket
- ✅ AI OS
- ❌ Desktop GUI
- ❌ Terminal CLI

**Best for:** Docker, systemd services, background processes

---

## 🔧 Command-Line Options

```bash
python main.py [OPTIONS]

Options:
  --gui              Force launch desktop GUI
  --no-gui           Disable desktop GUI
  --cli              Run CLI interface instead of GUI
  --api              API server only
  --headless         Run headless (no UI)
  --no-browser       Don't auto-open browser
  --host HOST        API server host (default: 0.0.0.0)
  --port PORT        API server port (default: 5000)
  --status           Show system status and exit
  --help             Show help message
```

### Examples
```bash
# Run with GUI on custom port
python main.py --port 8080

# Run on specific host (for network access)
python main.py --host 192.168.1.100

# Run headless for Docker
python main.py --headless --no-browser

# Show status only
python main.py --status

# Force GUI even if CLI specified
python main.py --gui --cli
```

---

## 📊 GUI Panels Explained

### System Metrics Panel
- **CPU Usage**: Percentage with progress bar
- **RAM Usage**: Percentage with progress bar
- **GPU Usage**: Percentage display
- **Disk Usage**: Percentage with progress bar
- **Network Speed**: Current throughput
- **System Uptime**: Time since boot

Updates every 1 second from `psutil`

### AI Core Visualization
- **Neural Activity**: Current neural network activity level (0-100%)
- **Learning Rate**: How fast the AI is learning (0-100%)
- **Memory Usage**: Used knowledge memory (percentage)
- **Knowledge Base**: Total stored knowledge in GB
- **Model Status**: Optimization level indicator

### Vision System Panel
- **Live Preview**: Placeholder for screen capture
- **Objects Detected**: Count of detected UI elements
- **YOLOv8 Status**: Detection model status

### Automation Engine Panel
- **Current Task**: Active automation task name
- **Progress Bar**: Visual progress indicator
- **Steps Completed**: X of Y steps
- **Status**: Running/Completed/Failed/Idle

### Commands Panel
- **Table Format**:
  - Time stamp
  - Command text
  - Execution status (Success/Running/Failed)
- **Scrollable History**: Last 50 commands
- **Status Colors**: Green=Success, Red=Failed, Blue=Running

### Memory & Context Panel
- **Memory Usage**: Current/Total
- **Total Memories**: Number of stored memories
- **Conversations**: Number of past conversations
- **User Interactions**: Tracked interactions count
- **Learning Progress**: Percentage learned

### Voice System Panel
- **Listen Button**: Toggle voice input
- **Status Display**: Current listening status
- **Status Colors**: Green=Listening, Gray=Idle

---

## 🔌 WebSocket Integration

The GUI automatically connects to the backend WebSocket server for real-time updates.

### Connection Status
- 🟢 **Green**: Connected and receiving data
- 🔴 **Red**: Disconnected
- 🟡 **Yellow**: Connecting

### Supported Messages
```json
{
  "type": "status",
  "data": {
    "version": "v2.0",
    "uptime": "00:15:30",
    "coreMode": "AUTONOMOUS"
  }
}
```

```json
{
  "type": "stats",
  "data": {
    "cpu": 23,
    "ram": 48,
    "gpu": 37,
    "internet": "Connected"
  }
}
```

```json
{
  "type": "command_status",
  "data": {
    "text": "Open YouTube",
    "status": "success"
  }
}
```

---

## 🛠️ Installation & Setup

### Requirements
- Python 3.8+
- PyQt5 5.15+
- websocket-client 1.3+
- psutil 5.9+

### Install
```bash
# Install all dependencies
pip install -r requirements.txt

# Or individually
pip install PyQt5 PyQtWebEngine websocket-client psutil
```

### Verify Installation
```bash
python test_gui.py
```

Should output:
```
✅ Desktop GUI module imported successfully
✅ All dependencies available
GUI can be launched with: python main.py
Or standalone with: python desktop_gui.py
```

---

## 🚨 Troubleshooting

### GUI doesn't appear
```bash
# Check PyQt5
python -c "from PyQt5.QtWidgets import QApplication; print('✅')"

# Force GUI launch
python main.py --gui --no-browser

# Check logs for errors
python main.py 2>&1 | Select-Object -Last 20  # PowerShell
python main.py 2>&1 | tail -20  # Linux/Mac
```

### WebSocket not connecting
- Check backend is running (look for "API server started")
- Verify port 8000 is available: `netstat -an | grep 8000`
- GUI will still work without WebSocket (shows local data)

### GUI freezes
- Close and reopen
- Check system resources (Task Manager)
- Restart the application
- Check `python main.py --status`

### Performance issues
- Close other applications
- Reduce GUI update frequency (edit `update_timer.start(1000)`)
- Run headless mode: `python main.py --headless`

---

## 📁 Files Modified/Created

### Core Files
- `main.py` - Updated with GUI launch logic
- `desktop_gui.py` - New desktop GUI implementation
- `requirements.txt` - Updated dependencies

### Launch Scripts
- `launch.bat` - Windows launcher
- `launch.sh` - Linux/Mac launcher
- `launch.py` - Python launcher

### Documentation
- `GUI_INTEGRATION.md` - Detailed integration guide
- `DESKTOP_GUI.md` - This file

---

## 🎯 Development

### Modify GUI Appearance
Edit `desktop_gui.py`:
```python
# Change colors, fonts, sizes
self.setStyleSheet("""
    QMainWindow {
        background-color: #020611;  # Dark background
    }
""")
```

### Add New Panels
1. Create new class inheriting from `NeonCard`
2. Implement `setup_ui()` method
3. Add to main grid layout in `RemoteControlWindow.setup_ui()`

### Customize Metrics
```python
# In SystemMetricsPanel.update_metrics()
cpu_percent = psutil.cpu_percent(interval=0.1)
# Add custom logic here
self.cpu_label.setText(f"CPU: {cpu_percent}%")
```

---

## 📈 Next Steps

1. **Run the system**: `python main.py`
2. **Watch the GUI**: Live metrics in real-time
3. **Test commands**: Send commands via GUI or web frontend
4. **Monitor logs**: Watch system events stream
5. **Experiment**: Try different features and modes

---

## 💡 Tips

✅ **Always run from project root**
```bash
cd ~/humanoid_assistant
python main.py
```

✅ **Keep terminal open** to see logs and errors

✅ **Use `--status`** to check system health without GUI
```bash
python main.py --status
```

✅ **Monitor resources** during long sessions

✅ **Gracefully close** with Ctrl+C or close GUI window

---

## 🔐 Security Notes

- GUI listens on localhost only by default
- WebSocket auth can be added (currently open for development)
- Consider adding authentication for production
- Network access disabled by default (use `--host 0.0.0.0` carefully)

---

## 📞 Support & Issues

For issues:
1. Check logs in terminal
2. Verify all dependencies installed
3. Test GUI separately: `python desktop_gui.py`
4. Check `test_gui.py` output
5. Review this guide thoroughly

---

**Happy automating! 🤖✨**

The desktop GUI is ready to use. Simply run `python main.py` and enjoy the futuristic dashboard!
