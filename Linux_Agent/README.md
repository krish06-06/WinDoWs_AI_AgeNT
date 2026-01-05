# Linux_Agent: Autonomous Linux Orchestration Engine

[![Linux](https://img.shields.io/badge/OS-Linux-1793D1?style=for-the-badge&logo=linux&logoColor=white)]
[![GNOME](https://img.shields.io/badge/Desktop-GNOME-4A86CF?style=for-the-badge&logo=gnome&logoColor=white)]
[![Wayland/X11](https://img.shields.io/badge/Display-Wayland%20%7C%20X11-orange?style=for-the-badge)]
[![Privacy](https://img.shields.io/badge/Privacy-Zero--Trust-blueviolet?style=for-the-badge)]
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

**Linux_Agent** is a privacy-first, autonomous AI orchestration engine designed for modern Linux desktops.  
It is a **sibling implementation** of the Windows agent, sharing the same philosophy, logic flow, and GUI, while adapting execution to Linux-specific environments such as GNOME, Wayland/X11, and Nix-based shells.

The agent prioritizes **local execution**, **low-latency interaction**, and **deep OS awareness**, avoiding cloud dependency wherever possible.

---

## 🌟 Key Pillars
- **Privacy-First:** Designed for local-first and eventual offline execution.
- **Cross-Display Compatible:** Works on GNOME with Wayland or X11 bridges.
- **Shared Intelligence Model:** Same DMM logic as Windows agent, OS-specific execution layer.
- **Shell-Oriented Execution:** Designed to run inside controlled Linux shells (e.g., `shell.nix`) instead of global system mutation.
- **Edge-Efficient:** Optimized for consumer hardware with GPU acceleration planned.

---

## 🧠 Execution Philosophy
Linux_Agent follows the same **Perception → Reasoning → Execution** pipeline as its Windows counterpart, but adapts execution to Linux tooling and permissions.

- **Speech-to-Text (STT):**  
  Selenium WebDriver–based STT for high accuracy and language robustness.

- **Decision-Making Model (DMM):**  
  Asynchronous, non-blocking intent reasoning shared across OS agents.

- **Execution Layer:**  
  Linux-native process control, filesystem interaction, application automation, and desktop-level actions.

> Architecture details are documented separately and intentionally not duplicated here.

---

## 🧰 Tech Stack
![Python](https://img.shields.io/badge/Language-Python%203.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Async](https://img.shields.io/badge/Concurrency-Asyncio-000000?style=for-the-badge)
![PyQt](https://img.shields.io/badge/GUI-PyQt5-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![Selenium](https://img.shields.io/badge/STT-Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Audio](https://img.shields.io/badge/TTS-Edge--TTS%20%2B%20pygame-yellow?style=for-the-badge)
![Linux](https://img.shields.io/badge/OS-Linux%20Automation-lightgrey?style=for-the-badge)

* **`Docs/Techstack.md`** For More Details

---

## 💻 Development Environment
Linux_Agent is actively developed and tested on the following environment:

| Component | Specification |
| :--- | :--- |
| **GPU** | NVIDIA GeForce RTX 4060 |
| **RAM** | 16GB Physical + Swap |
| **Desktop** | GNOME |
| **Display Server** | Wayland / X11 |
| **OS** | NixOS (shell-based execution) |
| **Audio Backend** | PulseAudio |
| **Inference Engine** | Planned (llama.cpp / ONNX) |

---

## 🔊 Audio & Speech
- **TTS:** Edge TTS with `pygame.mixer` playback
- **Backend:** PulseAudio (PipeWire-compatible environments expected)
- **Design Goal:** Minimal latency, OS-native audio routing

---

## 🔁 Relationship to Windows_Agent
Linux_Agent is **not a port** — it is a **sibling agent**.

- Same GUI (PyQt5)
- Same DMM logic
- Same privacy model
- Different execution bindings per OS

This allows features to evolve in parallel while respecting OS boundaries.

---

## 🚧 Project Status
🚧 **In active development**

Core features are functional, with continuous refinement of:
- Desktop automation reliability
- Audio stability across Wayland/X11
- Cross-distro compatibility (beyond NixOS shells)


---

## 📛 License & Attribution

Licensed under the **MIT License**.

If you use, fork, or redistribute this project or derivatives, please retain attribution:

**krish06-06 © 2026**

---

## 🛠 Installation & Quickstart
> ⚠️ **Warning**: This project is under active development.  
> ⚠️ Ensure all environment variables are provided via `.env` (see `example.env`). Do **not** commit secrets.

```bash
# Clone the monorepo
git clone https://github.com/krish06-06/OS-AGENT.git

# Enter Linux agent directory
cd OS-AGENT/Linux_Agent

# Enter development shell (example)
nix-shell

# Run the agent
python main.py

