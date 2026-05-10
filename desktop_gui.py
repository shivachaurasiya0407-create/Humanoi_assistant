#!/usr/bin/env python3
"""
Desktop GUI for Humanoid AI Assistant - PyQt5 Implementation
Matches the futuristic design with real-time system monitoring and AI visualization.
"""

import sys
import json
import threading
import time
from datetime import datetime
from typing import Optional, Dict, Any, Callable
import psutil

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit, QProgressBar, QScrollArea,
    QFrame, QGridLayout, QSplitter, QTabWidget, QTableWidget, QTableWidgetItem,
    QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QThread, QObject
from PyQt5.QtGui import QFont, QIcon, QColor, QPixmap, QImage

# Try to import WebSocket, but make it optional
try:
    import websocket
    WEBSOCKET_AVAILABLE = True
except ImportError:
    WEBSOCKET_AVAILABLE = False

# WebSocket data handler
class WebSocketThread(QThread):
    """Background thread for WebSocket connection."""
    data_received = pyqtSignal(dict)
    connection_changed = pyqtSignal(bool)
    
    def __init__(self, url: str = "ws://localhost:8000/ws"):
        super().__init__()
        self.url = url
        self.ws = None
        self.running = True
        self.available = WEBSOCKET_AVAILABLE
        
    def run(self):
        """Connect to WebSocket and receive messages."""
        if not self.available:
            self.connection_changed.emit(False)
            return
            
        try:
            self.ws = websocket.WebSocketApp(
                self.url,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close,
                on_open=self._on_open,
            )
            self.ws.run_forever()
        except Exception as e:
            print(f"WebSocket error: {e}")
            self.connection_changed.emit(False)
    
    def _on_open(self, ws):
        """Called when WebSocket opens."""
        self.connection_changed.emit(True)
    
    def _on_message(self, ws, message):
        """Called when message is received."""
        try:
            data = json.loads(message)
            self.data_received.emit(data)
        except json.JSONDecodeError:
            pass
    
    def _on_error(self, ws, error):
        """Called on error."""
        print(f"WebSocket error: {error}")
    
    def _on_close(self, ws, close_status_code, close_msg):
        """Called when WebSocket closes."""
        self.connection_changed.emit(False)
    
    def send_command(self, command: str):
        """Send a command via WebSocket."""
        if self.ws and self.available:
            try:
                self.ws.send(json.dumps({"type": "command", "text": command}))
            except Exception as e:
                print(f"Failed to send command: {e}")
    
    def stop(self):
        """Stop WebSocket connection."""
        self.running = False
        if self.ws and self.available:
            self.ws.close()


class NeonCard(QFrame):
    """Custom card widget with neon styling."""
    
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(10, 18, 36, 210);
                border: 1px solid rgba(96, 165, 250, 0.28);
                border-radius: 28px;
                padding: 20px;
            }
        """)
        self.setFrameShape(QFrame.StyledPanel)
        
        # Set size policy to expand
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        if title:
            title_label = QLabel(title)
            title_font = QFont("Segoe UI", 10)
            title_font.setLetterSpacing(QFont.PercentageSpacing, 130)
            title_label.setFont(title_font)
            title_label.setStyleSheet("color: #94a3b8; text-transform: uppercase;")
            self.layout.addWidget(title_label)


class SystemMetricsPanel(NeonCard):
    """Display real-time system metrics."""
    
    def __init__(self, parent=None):
        super().__init__("System Metrics", parent)
        
        self.metrics = {}
        self.setup_ui()
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_metrics)
        self.update_timer.start(1000)  # Update every second
    
    def setup_ui(self):
        """Setup UI components."""
        grid = QGridLayout()
        
        # CPU
        self.cpu_label = QLabel("CPU: 0%")
        self.cpu_progress = QProgressBar()
        self.cpu_progress.setStyleSheet("QProgressBar { border: none; border-radius: 5px; background: rgba(255, 255, 255, 0.08); }")
        self.cpu_progress.setTextVisible(False)
        grid.addWidget(QLabel("CPU Usage"), 0, 0)
        grid.addWidget(self.cpu_progress, 0, 1)
        grid.addWidget(self.cpu_label, 0, 2)
        
        # RAM
        self.ram_label = QLabel("RAM: 0%")
        self.ram_progress = QProgressBar()
        self.ram_progress.setStyleSheet("QProgressBar { border: none; border-radius: 5px; background: rgba(255, 255, 255, 0.08); }")
        self.ram_progress.setTextVisible(False)
        grid.addWidget(QLabel("RAM Usage"), 1, 0)
        grid.addWidget(self.ram_progress, 1, 1)
        grid.addWidget(self.ram_label, 1, 2)
        
        # GPU
        self.gpu_label = QLabel("GPU: 0%")
        grid.addWidget(QLabel("GPU Usage"), 2, 0)
        grid.addWidget(self.gpu_label, 2, 2)
        
        # Disk
        self.disk_label = QLabel("Disk: 0%")
        self.disk_progress = QProgressBar()
        self.disk_progress.setStyleSheet("QProgressBar { border: none; border-radius: 5px; background: rgba(255, 255, 255, 0.08); }")
        self.disk_progress.setTextVisible(False)
        grid.addWidget(QLabel("Disk Usage"), 3, 0)
        grid.addWidget(self.disk_progress, 3, 1)
        grid.addWidget(self.disk_label, 3, 2)
        
        # Network
        self.network_label = QLabel("Network: 0 Mbps")
        grid.addWidget(QLabel("Network Speed"), 4, 0)
        grid.addWidget(self.network_label, 4, 2)
        
        # Uptime
        self.uptime_label = QLabel("Uptime: 00:00:00")
        grid.addWidget(QLabel("System Uptime"), 5, 0)
        grid.addWidget(self.uptime_label, 5, 2)
        
        self.layout.addLayout(grid)
        self.layout.addStretch()
    
    def update_metrics(self):
        """Update system metrics."""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            ram_percent = psutil.virtual_memory().percent
            disk_percent = psutil.disk_usage('/').percent
            
            self.cpu_label.setText(f"CPU: {cpu_percent}%")
            self.cpu_progress.setValue(int(cpu_percent))
            
            self.ram_label.setText(f"RAM: {ram_percent}%")
            self.ram_progress.setValue(int(ram_percent))
            
            self.disk_label.setText(f"Disk: {disk_percent}%")
            self.disk_progress.setValue(int(disk_percent))
            
            # Try to get network stats
            net_io = psutil.net_io_counters()
            self.network_label.setText(f"Network: {net_io.bytes_sent / 1024 / 1024:.1f} MB/s")
            
        except Exception as e:
            pass  # Silently handle errors


class AICoreVisualization(NeonCard):
    """Display AI core 3D visualization."""
    
    def __init__(self, parent=None):
        super().__init__("AI Core - Neural Engine", parent)
        
        # Create a placeholder for 3D visualization
        self.viz_label = QLabel("🧠 Neural Network Activity")
        self.viz_label.setAlignment(Qt.AlignCenter)
        self.viz_label.setStyleSheet("color: #38bdf8; font-size: 14px;")
        self.viz_label.setMinimumHeight(300)
        
        # Stats
        stats_layout = QHBoxLayout()
        
        self.neural_activity = QLabel("Neural Activity: 78%")
        self.learning_rate = QLabel("Learning Rate: 63%")
        self.memory_usage = QLabel("Memory Usage: 51%")
        self.knowledge_base = QLabel("Knowledge Base: 2.7 GB")
        self.model_status = QLabel("Model Status: OPTIMAL")
        
        for label in [self.neural_activity, self.learning_rate, self.memory_usage, self.knowledge_base, self.model_status]:
            label.setStyleSheet("color: #e0f2fe;")
            stats_layout.addWidget(label)
        
        self.layout.addWidget(self.viz_label, 1)
        self.layout.addLayout(stats_layout)


class SystemStatusPanel(NeonCard):
    """Display system status."""
    
    def __init__(self, parent=None):
        super().__init__("System Status", parent)
        
        self.status_items = [
            ("AI Core", "ACTIVE"),
            ("Vision System", "ACTIVE"),
            ("Automation Engine", "ACTIVE"),
            ("Internet Agent", "ACTIVE"),
            ("Memory System", "ACTIVE"),
            ("Learning Engine", "ACTIVE"),
        ]
        
        for title, status in self.status_items:
            status_label = QLabel(f"● {title}: {status}")
            status_label.setStyleSheet(f"color: #10b981; font-weight: bold;")
            self.layout.addWidget(status_label)
        
        self.layout.addStretch()


class VisionPanel(NeonCard):
    """Display vision system data."""
    
    def __init__(self, parent=None):
        super().__init__("Vision System", parent)
        
        self.vision_display = QLabel("📷 Live Screen Analysis")
        self.vision_display.setAlignment(Qt.AlignCenter)
        self.vision_display.setStyleSheet("color: #94a3b8; font-size: 12px; min-height: 150px;")
        self.layout.addWidget(self.vision_display)
        
        info_layout = QHBoxLayout()
        self.objects_detected = QLabel("Objects Detected: 14")
        self.yolo_status = QLabel("YOLOv8: ACTIVE")
        self.objects_detected.setStyleSheet("color: #e0f2fe;")
        self.yolo_status.setStyleSheet("color: #e0f2fe;")
        info_layout.addWidget(self.objects_detected)
        info_layout.addStretch()
        info_layout.addWidget(self.yolo_status)
        self.layout.addLayout(info_layout)


class CommandsPanel(NeonCard):
    """Display command history and input."""
    
    def __init__(self, parent=None):
        super().__init__("Remote Commands", parent)
        
        self.commands_table = QTableWidget()
        self.commands_table.setColumnCount(3)
        self.commands_table.setHorizontalHeaderLabels(["Time", "Command", "Status"])
        self.commands_table.setStyleSheet("""
            QTableWidget {
                background-color: rgba(10, 18, 36, 0.5);
                color: #e0f2fe;
                border: none;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)
        self.layout.addWidget(self.commands_table)
        
        # Add sample commands
        sample_commands = [
            ("11:44:12", "Open YouTube and search AI", "Success"),
            ("11:43:21", "Take screenshot", "Success"),
            ("11:40:15", "Open VS Code", "Success"),
            ("11:38:47", "Run Python script", "Success"),
            ("11:31:10", "Shutdown in 10 minutes", "Success"),
        ]
        
        for i, (time, cmd, status) in enumerate(sample_commands):
            self.commands_table.insertRow(i)
            self.commands_table.setItem(i, 0, QTableWidgetItem(time))
            self.commands_table.setItem(i, 1, QTableWidgetItem(cmd))
            status_item = QTableWidgetItem(status)
            status_item.setForeground(QColor("#10b981"))
            self.commands_table.setItem(i, 2, status_item)
        
        self.commands_table.resizeColumnsToContents()


class AutomationPanel(NeonCard):
    """Display active automations."""
    
    def __init__(self, parent=None):
        super().__init__("Automation Engine", parent)
        
        self.current_task = QLabel("Current Task:")
        self.current_task.setStyleSheet("color: #94a3b8;")
        
        self.task_name = QLabel("Extracting data from website")
        self.task_name.setStyleSheet("color: #10b981; font-weight: bold;")
        
        self.progress_label = QLabel("Progress:")
        self.progress = QProgressBar()
        self.progress.setValue(75)
        self.progress.setStyleSheet("QProgressBar { border: none; border-radius: 5px; background: rgba(255, 255, 255, 0.08); }")
        self.progress.setTextVisible(False)
        
        self.steps = QLabel("Steps: 5 / 7")
        self.steps.setStyleSheet("color: #e0f2fe;")
        
        self.status = QLabel("Status: RUNNING")
        self.status.setStyleSheet("color: #10b981; font-weight: bold;")
        
        self.layout.addWidget(self.current_task)
        self.layout.addWidget(self.task_name)
        self.layout.addWidget(self.progress_label)
        self.layout.addWidget(self.progress)
        self.layout.addWidget(self.steps)
        self.layout.addWidget(self.status)
        self.layout.addStretch()


class LiveLogsPanel(NeonCard):
    """Display live system logs."""
    
    def __init__(self, parent=None):
        super().__init__("Live System Logs", parent)
        
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setStyleSheet("""
            QTextEdit {
                background-color: rgba(10, 18, 36, 0.5);
                color: #e0f2fe;
                border: none;
                font-family: 'Courier New';
                font-size: 9px;
            }
        """)
        
        sample_logs = [
            "[23:49:32] [AI CORE] System initialized successfully",
            "[23:45:33] [VISION] Screen captured - Objects detected: 14",
            "[23:45:34] [AUTOMATION] Task 'Extracting data from website' started",
            "[23:45:34] [INTERNET] Web agent navigating to target page",
            "[23:45:36] [MEMORY] New interaction saved to memory",
            "[23:45:37] [REMOTE] Command received from Web Control",
            "[23:45:38] [AI CORE] Response generated in 0.78s",
        ]
        
        self.logs_text.setText("\n".join(sample_logs))
        self.layout.addWidget(self.logs_text)


class MemoryPanel(NeonCard):
    """Display memory and context."""
    
    def __init__(self, parent=None):
        super().__init__("Memory & Context", parent)
        
        info_layout = QHBoxLayout()
        
        # Left side - Memory stats
        left = QVBoxLayout()
        left.addWidget(QLabel("Memory Usage: 2.7 GB / 5 GB"))
        left.addWidget(QLabel("Total Memories: 1,247"))
        left.addWidget(QLabel("Conversations: 342"))
        left.addWidget(QLabel("User Interactions: 28"))
        left.addWidget(QLabel("Learning Progress: 68.4%"))
        left.addStretch()
        
        # Right side - Brain visualization placeholder
        right = QVBoxLayout()
        brain_label = QLabel("🧠")
        brain_label.setAlignment(Qt.AlignCenter)
        brain_label.setStyleSheet("font-size: 60px;")
        right.addWidget(brain_label)
        
        info_layout.addLayout(left)
        info_layout.addLayout(right)
        self.layout.addLayout(info_layout)


class VoicePanel(NeonCard):
    """Display voice and audio system."""
    
    def __init__(self, parent=None):
        super().__init__("Voice & Audio System", parent)
        
        self.listen_btn = QPushButton("🎤 Start Listening")
        self.listen_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(56, 189, 248, 0.2);
                color: #38bdf8;
                border: 1px solid rgba(56, 189, 248, 0.3);
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(56, 189, 248, 0.3);
            }
        """)
        
        self.status_label = QLabel("Status: Listening...")
        self.status_label.setStyleSheet("color: #38bdf8;")
        
        self.layout.addWidget(self.listen_btn)
        self.layout.addWidget(self.status_label)
        self.layout.addStretch()


class RemoteControlWindow(QMainWindow):
    """Main window for remote control dashboard."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HUMAINOD AI - Remote Control Dashboard")
        
        # Get screen size and set appropriate window size
        screen = QApplication.primaryScreen().availableGeometry()
        screen_width = screen.width()
        screen_height = screen.height()
        
        # Set window size to 90% of screen size, max 1400x900
        window_width = min(int(screen_width * 0.9), 1400)
        window_height = min(int(screen_height * 0.9), 900)
        
        self.setGeometry(0, 0, window_width, window_height)
        self.setMinimumSize(1200, 700)  # Minimum size to ensure usability
        
        # If screen is small, maximize window
        if screen_width < 1400 or screen_height < 900:
            self.showMaximized()
        else:
            # Center the window on screen
            self.move((screen_width - window_width) // 2, (screen_height - window_height) // 2)
        
        print(f"GUI Window: Screen {screen_width}x{screen_height}, Window {window_width}x{window_height}, Maximized: {screen_width < 1400 or screen_height < 900}")
        
        # Dark theme stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #020611;
            }
            QLabel {
                color: #eef2ff;
            }
            QPushButton {
                background-color: rgba(59, 130, 246, 0.2);
                color: #38bdf8;
                border: 1px solid rgba(59, 130, 246, 0.3);
                border-radius: 8px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgba(59, 130, 246, 0.3);
            }
        """)
        
        # WebSocket thread
        self.ws_thread = WebSocketThread()
        self.ws_thread.data_received.connect(self.on_websocket_data)
        self.ws_thread.connection_changed.connect(self.on_connection_changed)
        self.ws_thread.start()
        
        self.setup_ui()
        self.ws_connected = False
    
    def setup_ui(self):
        """Setup the main UI."""
        print("Setting up GUI UI...")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Top bar
        top_layout = self.create_top_bar()
        main_layout.addLayout(top_layout)
        
        # Main content area with scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.1);
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: rgba(59, 130, 246, 0.5);
                border-radius: 6px;
            }
        """)
        
        content_widget = QWidget()
        content_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        scroll_area.setWidget(content_widget)
        
        # Main content grid
        content_layout = QHBoxLayout(content_widget)  # Changed to HBox for better column distribution
        
        # Left column - System panels
        left_col = self.create_left_column()
        content_layout.addLayout(left_col, 1)  # Equal stretch
        
        # Center column - AI Core and logs
        center_col = self.create_center_column()
        content_layout.addLayout(center_col, 1)  # Equal stretch
        
        # Right column - Control panels
        right_col = self.create_right_column()
        content_layout.addLayout(right_col, 1)  # Equal stretch
        
        main_layout.addWidget(scroll_area, 1)  # Give scroll area all remaining space
        print("GUI UI setup complete")
    
    def create_left_column(self):
        """Create the left column with system panels."""
        print("Creating left column...")
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # System Status Panel
        status_panel = SystemStatusPanel()
        status_panel.setMinimumHeight(200)
        layout.addWidget(status_panel)
        print("Added SystemStatusPanel")
        
        # System Metrics Panel
        metrics_panel = SystemMetricsPanel()
        metrics_panel.setMinimumHeight(250)
        layout.addWidget(metrics_panel)
        print("Added SystemMetricsPanel")
        
        # Automation Panel
        automation_panel = AutomationPanel()
        automation_panel.setMinimumHeight(200)
        layout.addWidget(automation_panel)
        print("Added AutomationPanel")
        
        layout.addStretch()  # Push panels to top
        print("Left column created")
        return layout
    
    def create_center_column(self):
        """Create the center column with AI core and logs."""
        print("Creating center column...")
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # AI Core Visualization
        ai_core = AICoreVisualization()
        ai_core.setMinimumHeight(300)
        layout.addWidget(ai_core)
        print("Added AICoreVisualization")
        
        # Live Logs Panel
        logs_panel = LiveLogsPanel()
        logs_panel.setMinimumHeight(200)
        layout.addWidget(logs_panel)
        print("Added LiveLogsPanel")
        
        print("Center column created")
        return layout
    
    def create_right_column(self):
        """Create the right column with control panels."""
        print("Creating right column...")
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Commands Panel
        commands_panel = CommandsPanel()
        commands_panel.setMinimumHeight(250)
        layout.addWidget(commands_panel)
        print("Added CommandsPanel")
        
        # Memory Panel
        memory_panel = MemoryPanel()
        memory_panel.setMinimumHeight(150)
        layout.addWidget(memory_panel)
        print("Added MemoryPanel")
        
        # Voice Panel
        voice_panel = VoicePanel()
        voice_panel.setMinimumHeight(100)
        layout.addWidget(voice_panel)
        print("Added VoicePanel")
        
        layout.addStretch()  # Push panels to top
        print("Right column created")
        return layout
    
    def create_top_bar(self) -> QVBoxLayout:
        """Create the top status bar."""
        top_layout = QVBoxLayout()
        
        # Main info bar
        info_layout = QHBoxLayout()
        
        title = QLabel("HUMAINOD AI")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: #e0f2fe;")
        
        version = QLabel("v2.0 OS")
        version.setFont(QFont("Segoe UI", 10))
        version.setStyleSheet("color: #94a3b8;")
        
        info_layout.addWidget(title)
        info_layout.addWidget(version)
        info_layout.addStretch()
        
        # Connection status
        self.connection_label = QLabel("● Connecting...")
        self.connection_label.setStyleSheet("color: #f59e0b;")
        info_layout.addWidget(self.connection_label)
        
        # Time
        self.time_label = QLabel()
        self.time_label.setStyleSheet("color: #94a3b8;")
        info_layout.addWidget(self.time_label)
        
        top_layout.addLayout(info_layout)
        
        # System stats bar
        stats_layout = QHBoxLayout()
        for label, metric in [("CPU", "23%"), ("RAM", "48%"), ("GPU", "37%"), ("Disk", "62%"), ("Network", "128 Mbps")]:
            stat = QLabel(f"{label}: {metric}")
            stat.setStyleSheet("color: #38bdf8; font-weight: bold;")
            stats_layout.addWidget(stat)
        
        top_layout.addLayout(stats_layout)
        
        # Update timer for time
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()
        
        return top_layout
    
    def update_time(self):
        """Update the time display."""
        current_time = datetime.now()
        time_str = current_time.strftime("%I:%M:%S %p")
        date_str = current_time.strftime("%A, %B %d, %Y")
        self.time_label.setText(f"{time_str} - {date_str}")
    
    def on_websocket_data(self, data: dict):
        """Handle data from WebSocket."""
        # Process received data
        pass
    
    def on_connection_changed(self, connected: bool):
        """Handle connection status change."""
        self.ws_connected = connected
        if connected:
            self.connection_label.setText("● Connected")
            self.connection_label.setStyleSheet("color: #10b981;")
        else:
            self.connection_label.setText("● Disconnected")
            self.connection_label.setStyleSheet("color: #ef4444;")
    
    def closeEvent(self, event):
        """Handle window close."""
        if self.ws_thread.isRunning():
            self.ws_thread.stop()
            self.ws_thread.quit()
            self.ws_thread.wait()
        event.accept()


def run_desktop_gui():
    """Run the desktop GUI application."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    window = RemoteControlWindow()
    window.show()
    
    return app, window


def run_gui_in_thread():
    """Run GUI in a separate daemon thread without blocking."""
    try:
        from PyQt5.QtWidgets import QApplication
        
        # Create or get existing app
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Create and show window
        window = RemoteControlWindow()
        window.show()
        
        # Process events without blocking indefinitely
        while True:
            app.processEvents()
            time.sleep(0.05)  # 50ms interval to prevent CPU spin
    except Exception as e:
        print(f"GUI Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    app, window = run_desktop_gui()
    sys.exit(app.exec_())
