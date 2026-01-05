import sys
import os
import threading
import asyncio
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QThread
from dotenv import load_dotenv


# Ensures the script can see the Backend and Frontend folders correctly
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Internal Imports using absolute paths
from Frontend.helpers import (
    get_assis, set_assis, Setmicrophonestatus, 
    getmicrophonedata, querymodif
)
from Backend.STT import SpeechRecognition

# Load Env
load_dotenv(BASE_DIR / ".env")
USERNAME = os.getenv("Username", "User")
ASSIS_NAME = os.getenv("assis_name", "Assistant")

class BackendWorker(QObject):
    """Handles AI logic in a background thread to prevent GUI freezing."""
    finished_response = pyqtSignal(str, str) 

    def run_query(self, text):
        try:
            # Lazy import to avoid circular dependency with main.py
            from main import MainExecution 
            
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Run the actual AI logic
            answer = loop.run_until_complete(MainExecution(text))
            self.finished_response.emit(text, answer)
            loop.close()
        except Exception as e:
            print(f"Backend Error: {e}")
            self.finished_response.emit(text, f"Sorry, I encountered an error: {e}")

class JordGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
        # Setup Background Threading
        self.thread = QThread()
        self.worker = BackendWorker()
        self.worker.moveToThread(self.thread)
        self.worker.finished_response.connect(self.display_chat)
        self.thread.start()

    def initUI(self):
        self.setWindowTitle(f"{ASSIS_NAME} AI - Desktop Assistant")
        self.resize(500, 700)
        
        self.setStyleSheet("""
            QWidget { background-color: #121212; color: #E0E0E0; }
            QTextEdit { background-color: #1E1E1E; border: 1px solid #333; border-radius: 8px; font-size: 14px; padding: 10px; }
            QLineEdit { background-color: #2B2B2B; border: 1px solid #444; padding: 8px; border-radius: 5px; }
            QPushButton#voiceBtn { background-color: #00E5FF; color: #000; font-weight: bold; border-radius: 5px; }
            QPushButton#stopBtn { background-color: #FF3D00; color: #FFF; border-radius: 5px; }
        """)

        layout = QVBoxLayout(self)

        self.title = QLabel(ASSIS_NAME.upper())
        self.title.setFont(QFont("Arial", 18, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: #00E5FF; margin: 10px;")
        layout.addWidget(self.title)

        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        self.status_label = QLabel("Status: Ready")
        self.status_label.setStyleSheet("color: #888; font-size: 11px;")
        layout.addWidget(self.status_label)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type a command and press Enter...")
        self.input_field.returnPressed.connect(self.handle_text_input)
        layout.addWidget(self.input_field)

        btn_layout = QHBoxLayout()
        self.voice_btn = QPushButton("🎤 Voice Mode")
        self.voice_btn.setObjectName("voiceBtn")
        self.voice_btn.setMinimumHeight(40)
        self.voice_btn.clicked.connect(self.handle_voice_input)
        
        self.stop_btn = QPushButton("🛑 Stop")
        self.stop_btn.setObjectName("stopBtn")
        self.stop_btn.setMinimumHeight(40)
        self.stop_btn.clicked.connect(self.stop_listening)

        btn_layout.addWidget(self.voice_btn)
        btn_layout.addWidget(self.stop_btn)
        layout.addLayout(btn_layout)

    def display_chat(self, user_text, ai_response):
        user_html = f'<div style="margin-bottom: 10px;"><b>{USERNAME}:</b> {user_text}</div>'
        ai_html = f'<div style="margin-bottom: 15px; color: #00E5FF;"><b>{ASSIS_NAME}:</b> {ai_response}</div>'
        self.chat_display.append(user_html)
        self.chat_display.append(ai_html)
        self.status_label.setText("Status: Ready")

    def handle_text_input(self):
        text = self.input_field.text().strip()
        if text:
            self.input_field.clear()
            self.status_label.setText(f"Status: Thinking...")
            # Run query in background thread
            threading.Thread(target=self.worker.run_query, args=(text,), daemon=True).start()

    def handle_voice_input(self):
        self.status_label.setText("Status: Listening...")
        Setmicrophonestatus("True")
        
        def listen_task():
            # SpeechRecognition() blocks until it hears something
            query = SpeechRecognition() 
            if query:
                self.worker.run_query(query)
            else:
                self.status_label.setText("Status: No speech detected")
        
        threading.Thread(target=listen_task, daemon=True).start()

    def stop_listening(self):
        Setmicrophonestatus("False")
        self.status_label.setText("Status: Stopped")

def launch_gui():
    app = QApplication(sys.argv)
    # This is critical for Wayland: it tells Qt which app name to show in the dock
    app.setApplicationName(ASSIS_NAME)
    win = JordGUI()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    launch_gui()