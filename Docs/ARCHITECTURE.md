# OS-Agent Architecture: Cross-OS AI Assistant

[![Linux](https://img.shields.io/badge/OS-Linux%20%2F%20Windows-FF6F00?style=for-the-badge&logo=linux&logoColor=white)](https://www.linux.org)  
[![Python](https://img.shields.io/badge/Language-Python%203.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)  
[![Async](https://img.shields.io/badge/Concurrency-Asyncio-000000?style=for-the-badge)](https://docs.python.org/3/library/asyncio.html)  
[![Privacy](https://img.shields.io/badge/Privacy-Zero--Trust-blueviolet?style=for-the-badge)](https://github.com/krish06-06/OS-AGENT)

---

## 🌟 Overview

**OS-Agent** is a **cross-platform, local-first AI assistant** compatible with:

- **Linux** (NixOS, GNOME, Wayland/X11)  
- **Windows** (Windows 11 Pro/Enterprise)

It handles **voice & text input**, reasoning, OS automation, and optional web integration.  

The architecture ensures **modularity, fault isolation, and safe execution**, allowing the same agent to work seamlessly across multiple operating systems.

---

## 🏗️ High-Level System Flow

### Voice Input Flow

User (Voice) → STT Engine → Decision-Making Model (DMM) → Chatbot / Search / Automation / Image Generation → TTS → GUI Update

### Text Input Flow

User (Text) → DMM → Chatbot / Search / Automation / Image Generation → GUI Update → Optional TTS

> **Difference:** Only the input acquisition changes (Voice vs Text).

---

## 🧩 Core Components

### 1️⃣ Entry Point (`main.py`)

- Central orchestrator of the agent  
- Initializes environment & event loop  
- Manages **frontend/backend threading**  
- Controls **STT activation** and graceful shutdown  

### 2️⃣ Frontend (`Frontend/`)

- **GUI:** PyQt5 cross-platform interface  
- **Helpers:** Shared state management (mic status, assistant status)  
- **File-based communication:** For long-running tasks like image generation  
- **Cross-OS Compatible:** Uses Qt + X11/Wayland bridges on Linux, native APIs on Windows  

### 3️⃣ Backend (`Backend/`)

Contains all **reasoning and execution logic**.

#### 3.1 Speech-to-Text (`STT.py`)

- Selenium-based web STT engine (Linux/Windows)  
- High-accuracy transcription  
- On-demand activation only  

#### 3.2 Decision-Making Model (`Model.py`)

- Classifies input intents: `general`, `realtime`, `open/close`, `generate`, `exit`  
- Purely logical — does not execute OS actions  

#### 3.3 Chatbot (`Chatbot.py`)

- Handles general conversational responses  
- Triggered when DMM labels input as `general`  

#### 3.4 Real-Time Search (`Realtimesearchengine.py`)

- Triggered when DMM labels input as `realtime`  
- Optional internet-based answers (Google search, API)  

#### 3.5 Automation (`Automation.py`)

- Executes OS-level actions:
  - Launch/close apps  
  - Browser control  
  - File system tasks  
- Only allowed actions based on DMM intent  

#### 3.6 Image Generation (`ImageGeneratic.py`)

- API-based image synthesis  
- Runs in **subprocess** to avoid blocking main loop  

#### 3.7 Text-to-Speech (`TTS.py`)

- Converts responses to voice  
- Async execution after response generation  

---

## 4️⃣ Data Layer (`Data/`)

Stores **runtime-generated artifacts**, not logic:

- `chatlog.json` – Persistent conversation history  
- `image_gen/` – Generated images  
- `letters/` – Generated text outputs  
- `speech.mp3` – TTS audio  
- `Voice.html` – Voice assets  

> Acts as **memory, cache, and output storage**.

---

## 🔄 Async & Threading Model

- GUI runs on main thread  
- Backend logic runs in **daemon background thread**  
- Async event loop handles:
  - STT  
  - Decision-making  
  - Automation  
  - TTS  

**Benefits:**  
- No GUI freezing  
- Controlled microphone activation  
- Predictable execution  

---

## 🔐 Execution Safety Model

- All actions pass through:
  1. Model classification  
  2. Intent validation  
- OS actions limited to predefined safe functions  

---

## 🌐 System Mode

- **Hybrid architecture**  
- **Local-first reasoning**  
- Optional internet for:
  - Real-time search  
  - API-based image generation  

---

## ❌ Non-Goals

- Fully autonomous background execution  
- Hidden telemetry or data collection  
- Remote system control  

---

## ✅ Summary

This architecture ensures **cross-OS compatibility**, clean separation of GUI, intelligence, and execution, and a **safe, modular AI assistant** capable of running on Linux and Windows with near-identical behavior.  

For roadmap and future features, see `Docs/RoadMap.md`.
