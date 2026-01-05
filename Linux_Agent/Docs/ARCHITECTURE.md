# WinDoWs_AI_AgeNT

## Overview

This project is a **hybrid, local-first AI Assistant for Windows**, designed to handle voice and text interactions, reason about user intent, and execute system-level or informational tasks through a modular backend.

The architecture is intentionally split into **Frontend**, **Backend (Intelligence & Execution)**, and **Data** layers to maintain clarity, extensibility, and fault isolation.

---

## High-Level System Flow

### Voice Input Flow

User (Voice)
→ STT (SpeechRecognition)
→ Model (FirstlayerDMM)
→ Chatbot / Search / Automation / Image Generation
→ TTS (Text_to_speech)
→ GUI Chat Screen Update

### Text Input Flow

User (Text)
→ Model (FirstlayerDMM)
→ Chatbot / Search / Automation / Image Generation
→ GUI Chat Screen Update
→ (Optional) TTS

The only difference between voice and text input is the **input acquisition stage** (STT vs direct text).

---

## Core Components

## 1. Entry Point (main.py)

`main.py` acts as the **central orchestrator** of the entire system.

### Responsibilities

* Application bootstrap
* Environment setup
* Frontend & backend coordination
* Async event-loop management
* Thread management
* Graceful shutdown handling

### Key Characteristics

* Runs an **async decision pipeline** inside a background thread
* Launches the GUI on the main thread
* Controls when STT is activated via shared frontend state

---

## 2. Frontend Layer (`Frontend/`)

The frontend is responsible for **user interaction and state signaling**, not intelligence.

### Files

* `gui.py` – PyQt-based GUI (chat screen, mic toggle)
* `helpers.py` – Shared state utilities (mic status, assistant status, screen updates)
* `Files/` – Runtime data exchange files (e.g., image generation triggers)
* `Graphics/` – UI assets

### Frontend ↔ Backend Communication

* Direct Python imports
* Shared state via helper functions
* File-based signaling for long-running tasks (e.g., image generation)

The frontend **never performs reasoning or OS actions**.

---

## 3. Backend Layer (`Backend/`)

The backend contains all intelligence, reasoning, and execution logic.

### 3.1 Speech-to-Text (STT.py)

* Activated only when microphone status is enabled
* Converts live speech into text queries
* Includes browser automation cleanup utilities

STT runs **on-demand**, not continuously.

---

### 3.2 Decision-Making Model (`Model.py`)

This file represents the **thinking layer** of the assistant.

### Responsibilities

* Classify user input
* Output structured intent labels such as:

  * `general`
  * `realtime`
  * `open / close`
  * `generate`
  * `exit`

The model does **not execute actions** — it only decides *what should happen*.

---

### 3.3 Chatbot (`Chatbot.py`)

* Handles general conversational responses
* Used when the DMM classifies input as `general`
* Does not access OS or system resources

---

### 3.4 Real-Time Search (`Realtimesearchengine.py`)

* Triggered when the DMM marks a query as `realtime`
* Used for fresh or internet-based answers (e.g., Google search)
* Optional and internet-dependent

---

### 3.5 Automation (`Automation.py`)

Responsible for **system-level actions**.

### Scope

* Opening / closing applications
* Browser control
* OS-level commands

Automation is only triggered if:

* The DMM classifies the intent correctly
* The intent matches allowed function prefixes

---

### 3.6 Image Generation (`ImageGeneratic.py`)

* API-based image generation
* Triggered by the DMM when `generate` intent is detected
* Executed as a **separate subprocess**

This prevents blocking the main assistant loop.

---

### 3.7 Text-to-Speech (`TTS.py`)

* Converts final responses into speech
* Always active when enabled
* Executed asynchronously after response generation

---

## 4. Data Layer (`Data/`)

The Data directory stores **runtime-generated artifacts**, not logic.

### Contents

* `chatlog.json` – Persistent conversation history
* `image_gen/` – Generated images
* `letters/` – Generated text outputs
* `speech.mp3` – TTS audio output
* `Voice.html` – Voice-related assets

This layer acts as **memory, cache, and output storage**.

---

## Asynchronous & Threading Model

* GUI runs on the main thread
* Backend logic runs in a daemon background thread
* Async event loop handles:

  * STT
  * Decision-making
  * Automation
  * TTS

This design ensures:

* No GUI freezing
* Controlled microphone activation
* Predictable execution flow

---

## Execution Safety Model

* No direct execution from raw user input
* All actions must pass through:

  1. Model classification
  2. Explicit intent validation
* OS actions are limited to predefined functions

---

## System Mode

* **Hybrid architecture**
* Local-first reasoning
* Optional internet usage for:

  * Real-time search
  * API-based image generation

---

## Non-Goals

* Fully autonomous background execution
* Hidden telemetry or data collection
* Remote system control

---

## Summary

This architecture enables a **clean separation between interface, intelligence, and execution**, allowing the assistant to scale from a basic AI chatbot into a powerful Windows AI agent while maintaining control, safety, and clarity.

For future plans, refer to `Docs/RoadMap.md`.
