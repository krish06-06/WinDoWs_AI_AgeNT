# Windows_Agent: Autonomous Windows Orchestration Engine

[![Windows 11](https://img.shields.io/badge/OS-Windows%2011-0078D4?style=for-the-badge&logo=windows-11&logoColor=white)](https://www.microsoft.com/windows)
[![NVIDIA](https://img.shields.io/badge/GPU-NVIDIA%20RTX%204060-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](https://www.nvidia.com/en-us/geforce/graphics-cards/40-series/rtx-4060-4060ti/)
[![Privacy](https://img.shields.io/badge/Privacy-Zero--Trust-blueviolet?style=for-the-badge)]([https://github.com/krish06-06/WinDoWs_AI_AgeNTos-agent](https://github.com/krish06-06/WinDoWs_AI_AgeNT))
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

WinDoWs_AI_AgeNT is a high-performance, privacy-centric AI entity designed for comprehensive Windows OS management. By decoupling the **Decision-Making Model (DMM)** from the **Speech-to-Text (STT)** engine, this agent provides a low-latency, "Zero-Trust" environment that prioritizes local hardware utilization over cloud dependency.

## 🌟 Key Pillars
- **Privacy-First:** Designed for eventual 100% offline execution.
- **Asynchronous Logic:** Non-blocking DMM architecture for fluid user interaction.
- **System Integration:** Deep-level OS automation ranging from file-system hygiene to network management.
- **Edge Efficiency:** Optimized for consumer-grade GPUs (RTX 4060) to provide enterprise-level automation.

## 🏗️ Technical Architecture
The system operates on a modular pipeline designed for the Windows 11 ecosystem:
* **Perception:** Hybrid Web-Native STT Engine for high-accuracy vocal capture.
* **Reasoning:** Asynchronous Decision-Making Model (DMM) for intent parsing.
* **Execution:** Surgical background process management and native Windows API integration.

* For Details, refer to **`Docs/ARCHITECTURE.md`**

---
## 🧰 Tech Stack
![Python](https://img.shields.io/badge/Language-Python%203.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Async](https://img.shields.io/badge/Concurrency-Asyncio-000000?style=for-the-badge)
![JSON](https://img.shields.io/badge/Data-JSON-lightgrey?style=for-the-badge)
![PyQt](https://img.shields.io/badge/GUI-PyQt5-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![Windows](https://img.shields.io/badge/OS-Windows%2011%20API-0078D4?style=for-the-badge&logo=windows&logoColor=white)
![Selenium](https://img.shields.io/badge/Web-Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)

* **`Docs/Techstack.md`** For More Details

## 💻 Development Environment
To ensure maximum performance and reproducibility, the project is developed and tested on the following stack:

| Component | Specification |
| :--- | :--- |
| **GPU** | NVIDIA GeForce RTX 4060  |
| **RAM** | 16GB Physical + System-Managed Swap |
| **Operating System** | Windows 11 Pro |
| **Inference Engine** | Planned migration to Llama.cpp / ONNX |

---

## 🔁 Relationship to Linux_Agent
Windows_Agent is **not a port** — it is a **sibling agent**.

- Same GUI (PyQt5)
- Same DMM logic
- Same privacy model
- Different execution bindings per OS

This allows features to evolve in parallel while respecting OS boundaries.

---

## Project Status
🚧 In progress......

## Roadmap
See **`Docs/RoadMap.md`** For project roadmap.

---

## 📛 License & Attribution

Licensed under the **MIT License**.

If you use, fork, or redistribute this project or derivatives, please retain attribution:

**krish06-06 © 2026**

---

## 🛠 Installation & Quickstart
> ⚠️**Warning**: This project is in active development. Ensure you are using the latest version of this agent.</br>
> ⚠️**Warning**: Make sure to create a `.env` file with your API keys Respective to `example.env`. Do **not** include them in GitHub.

```powershell
# Clone the repository
git clone https://github.com/krish06-06/OS-AGENT.git


# Enter project directory
cd {project_name}

# Install dependencies (Example)
pip install -r Requirements.txt

