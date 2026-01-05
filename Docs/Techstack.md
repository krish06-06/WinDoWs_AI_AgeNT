## 🧰 Tech Stack (Cross-OS)

### 🧠 Core Language & Runtime
![Python](https://img.shields.io/badge/Language-Python%203.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Async](https://img.shields.io/badge/Concurrency-Asyncio-000000?style=for-the-badge)

- **Python 3.11** – Core orchestration, reasoning, and execution  
- **Asyncio** – Non-blocking decision-making and task execution  
- **Threading** – GUI and backend concurrency management  

---

### 🎙️ Speech & Audio Processing
![STT](https://img.shields.io/badge/STT-Selenium-WebDriver-FF6F00?style=for-the-badge)
![Audio](https://img.shields.io/badge/Audio-Edge--TTS%20%2B%20PyGame-4CAF50?style=for-the-badge)

- **Speech-to-Text (STT)**  
  - Windows & Linux: Selenium WebDriver–based STT for high-accuracy recognition  
- **Text-to-Speech (TTS)**  
  - Edge TTS with `pygame.mixer` playback (cross-OS)  
- **Audio Backend**  
  - Windows: Native audio APIs  
  - Linux: PulseAudio (Wayland/X11 compatible)  
- **Silence Detection** – End-of-speech detection  
- **Hybrid Playback & Recording** – Local-first, OS-native audio handling  

---

### 🧠 Intelligence & Reasoning
![AI](https://img.shields.io/badge/AI-Decision%20Making%20Model-purple?style=for-the-badge)

- **Decision-Making Model (DMM)** – Intent classification (`Model.py`)  
- **Chatbot Engine** – Conversational responses  
- **Rule-based + Model-driven Routing** – Action selection logic  

---

### 🌐 Real-Time Intelligence
![Search](https://img.shields.io/badge/Search-RealTime%20Engine-blue?style=for-the-badge)

- **Real-Time Search Engine** – Internet-backed responses  
- **Hybrid Execution** – Local-first with optional web access  

---

### ⚙️ Desktop & Automation
![Windows](https://img.shields.io/badge/OS-Windows%2011%20API-0078D4?style=for-the-badge&logo=windows&logoColor=white)
![Linux](https://img.shields.io/badge/OS-Linux-lightgrey?style=for-the-badge)
![GNOME](https://img.shields.io/badge/Desktop-GNOME-4A86CF?style=for-the-badge)
![Wayland/X11](https://img.shields.io/badge/Display-Wayland%20%7C%20X11-orange?style=for-the-badge)
![Selenium](https://img.shields.io/badge/Web-Selenium-43B02A?style=for-the-badge)

- **PyQt5 GUI** – Chat-style interface on Windows & Linux  
- **Desktop Automation**  
  - Windows: Native API & subprocess management  
  - Linux: Wayland/X11 compatible via `xdotool` & system commands  
- **Filesystem / App Control** – Automates searches, apps, basic file ops  
- **Browser Automation** – Selenium WebDriver (cross-OS)  
- **Shell-Oriented Execution (Linux)** – Managed via `shell.nix` for reproducibility  

---

### 🖼️ Media & Generation
![Image](https://img.shields.io/badge/Image%20Generation-API--Based-orange?style=for-the-badge)

- **Image Generation Module** – API-based image synthesis  
- **Subprocess Isolation** – Non-blocking execution  

---

### 🖥️ Frontend & Interface
![PyQt](https://img.shields.io/badge/GUI-PyQt5-41CD52?style=for-the-badge&logo=qt&logoColor=white)

- **Cross-OS PyQt5 GUI** – Live assistant interface  
- **Live Status Indicators** – Mic, TTS, and assistant state  
- **Frontend–Backend Bridge** – Shared state helpers  

---

### 📁 Data & Persistence
![JSON](https://img.shields.io/badge/Data-JSON-lightgrey?style=for-the-badge)

- **Chat Logs** – Persistent conversation history  
- **Generated Assets** – Images, audio, text  
- **File-based State Sync** – Lightweight cross-module data exchange  

---

### 🔐 Security & Privacy
![Privacy](https://img.shields.io/badge/Privacy-Zero--Trust-blueviolet?style=for-the-badge)

- **Zero-Trust Execution Flow** – Local-first processing  
- **Environment-based Secrets (`.env`)**  
- **Hybrid Mode** – Internet access only when required  

---

### 🔮 Planned / Future Stack
![LLM](https://img.shields.io/badge/LLM-LLaMA.cpp%20%2F%20ONNX-8A2BE2?style=for-the-badge)

- **LLaMA.cpp** – Local LLM inference (Windows & Linux)  
- **ONNX Runtime** – Optimized cross-platform execution  
- **Plugin-based Skill System** – Extensible actions across OS agents
