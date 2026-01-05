import sys
import os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
import threading
import asyncio
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QThread
from dotenv import dotenv_values

# Internal Imports
from Frontend.helpers import (
    get_assis, set_assis, Setmicrophonestatus, 
    getmicrophonedata, querymodif
)
from Backend.STT import SpeechRecognition



# Setup Paths
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAPHICS_PATH = os.path.join(ROOT_DIR, "Frontend", "Graphics")

env_vars = dotenv_values(".env")
USERNAME = env_vars.get("Username", "User")
ASSIS_NAME = env_vars.get("assis_name", "Assistant")

class BackendWorker(QObject):
    """Handles AI logic in a background thread to prevent GUI freezing."""
    finished_response = pyqtSignal(str, str) # Sends (User Query, AI Response)

    def run_query(self, text):
        # Run the async backend in a synchronous-friendly way for the thread
        from main import MainExecution #To prevent Circular call problem
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # This calls your main.py logic
        answer = loop.run_until_complete(MainExecution(text))
        self.finished_response.emit(text, answer)

class JordGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.worker = BackendWorker()
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.worker.finished_response.connect(self.display_chat)
        self.thread.start()

    def initUI(self):
        self.setWindowTitle(f"{ASSIS_NAME} AI - Desktop Assistant")
        self.resize(500, 700)
        self.setStyleSheet("background-color: #121212; color: white;")

        layout = QVBoxLayout(self)

        # Title
        self.title = QLabel(ASSIS_NAME.upper())
        self.title.setFont(QFont("Arial", 16, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("color: #00e5ff; margin-bottom: 10px;")
        layout.addWidget(self.title)

        # Chat Display
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet("background-color: #1e1e1e; border-radius: 10px; padding: 10px; border: 1px solid #333;")
        layout.addWidget(self.chat_display)

        # Status Label
        self.status_label = QLabel("Status: Ready")
        self.status_label.setStyleSheet("color: #888; font-size: 11px;")
        layout.addWidget(self.status_label)

        # Input Field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type a command...")
        self.input_field.setStyleSheet("padding: 10px; background: #2b2b2b; border-radius: 5px;")
        self.input_field.returnPressed.connect(self.handle_text_input)
        layout.addWidget(self.input_field)

        # Buttons Layout
        btn_layout = QHBoxLayout()
        
        self.voice_btn = QPushButton("🎤 Voice Mode")
        self.voice_btn.setStyleSheet("background-color: #00e5ff; color: black; font-weight: bold; padding: 10px; border-radius: 5px;")
        self.voice_btn.clicked.connect(self.handle_voice_input)
        
        self.stop_btn = QPushButton("🛑 Stop STT")
        self.stop_btn.setStyleSheet("background-color: #ff3d00; color: white; padding: 10px; border-radius: 5px;")
        self.stop_btn.clicked.connect(self.stop_listening)

        btn_layout.addWidget(self.voice_btn)
        btn_layout.addWidget(self.stop_btn)
        layout.addLayout(btn_layout)

    def display_chat(self, user_text, ai_response):
        """Updates the chat screen with formatted HTML."""
        user_html = f'<div style="margin: 5px;"><b>{USERNAME}:</b> {user_text}</div>'
        ai_html = f'<div style="margin: 5px; color: #00e5ff;"><b>{ASSIS_NAME}:</b> {ai_response}</div>'
        self.chat_display.append(user_html)
        self.chat_display.append(ai_html)
        self.status_label.setText("Status: Ready")

    def handle_text_input(self):
        text = self.input_field.text().strip()
        if text:
            self.input_field.clear()
            self.status_label.setText(f"Status: {ASSIS_NAME} is thinking...")
            # Trigger the background worker
            threading.Thread(target=self.worker.run_query, args=(text,), daemon=True).start()

    def handle_voice_input(self):
        """Triggers the STT module."""
        self.status_label.setText("Status: Listening...")
        Setmicrophonestatus("True")
        
        def listen_task():
            query = SpeechRecognition() # This uses your Selenium-based STT
            if query:
                self.worker.run_query(query)
        
        threading.Thread(target=listen_task, daemon=True).start()

    def stop_listening(self):
        Setmicrophonestatus("False")
        self.status_label.setText("Status: STT Stopped")

def launch_gui():
    app = QApplication(sys.argv)
    win = JordGUI()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    launch_gui()