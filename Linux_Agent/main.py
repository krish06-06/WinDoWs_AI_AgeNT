import os
import sys
import json
import time
import asyncio
import threading
import subprocess
from pathlib import Path
from dotenv import dotenv_values

# --- Internal Module Imports ---
from Frontend.helpers import (
    get_assis, set_assis, getmicrophonedata, Setmicrophonestatus,
    Answermodif, showtexttoscreen, temp_dir_path, querymodif
)
from Frontend.gui import launch_gui
from Backend.Model import FirstlayerDMM
from Backend.Realtimesearchengine import realtimesearchengine
from Backend.Automation import Automation
from Backend.STT import SpeechRecognition, stop_assistant_chrome, driver
from Backend.Chatbot import chatbot
from Backend.TTS import Text_to_speech

# --- Environment Setup ---

BASE_DIR = Path(__file__).resolve().parent
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

env_vars = dotenv_values(BASE_DIR / ".env")
username = env_vars.get("Username", "User")
assis_name = env_vars.get("assis_name", "Assistant")

Defaultmessage = f"{username}: Hello {assis_name}.\n{assis_name}: Welcome! I am online and ready to help."
Functions = ["open", "close", "google search"]

# --- Chat Log Logic ---
def ReadChatLogJson():
    path = BASE_DIR / "Data" / "Chatlog.json"
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data if data else [{"role": "assistant", "content": Defaultmessage}]
    except (FileNotFoundError, json.JSONDecodeError):
        return [{"role": "assistant", "content": Defaultmessage}]

def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    for entry in json_data:
        role = entry["role"].lower()
        content = entry['content']
        if role == "user":
            formatted_chatlog += f"{username}: {content}\n"
        else:
            formatted_chatlog += f"{assis_name}: {content}\n"
    
    with open(temp_dir_path('Database.data'), 'w', encoding='utf-8') as file:
        file.write(Answermodif(formatted_chatlog))

def ShowChatsOnGUI():
    try:
        with open(temp_dir_path('Database.data'), "r", encoding="utf-8") as file:
            Data = file.read()
        if Data.strip():
            showtexttoscreen(Data)
    except Exception as e:
        print(f"GUI Sync Error: {e}")

def InitialExecution():
    Setmicrophonestatus("False")
    ChatLogIntegration()
    ShowChatsOnGUI()
    set_assis("Available ...")

# --- Core AI Logic ---
async def MainExecution(Query: str = None):
    ActionExecuted = False
    Answer = ""

    if Query is None:
        set_assis("Listening ...")
        Query = SpeechRecognition()
    
    if not Query:
        set_assis("Available ...")
        return ""

    # Intent Classification
    Decision = FirstlayerDMM(Query)
    Decision = [str(i) for i in (Decision if isinstance(Decision, list) else [Decision])]

    # Task Sorting Flags
    is_realtime = any(i.startswith("realtime") for i in Decision)
    is_general = any(i.startswith("general") for i in Decision)
    is_image = any("generate" in i for i in Decision)
    is_exit = any(i.startswith("exit") for i in Decision)

    # 1. Exit Logic
    if is_exit:
        Answer = "Goodbye! I am shutting down."
        await Text_to_speech(Answer)
        print("Finalizing shutdown...")
        driver.quit()
        stop_assistant_chrome()
        os._exit(0)

    # 2. Automation check
    for q in Decision:
        if any(q.startswith(f) for f in Functions):
            success = await Automation(Decision)
            Answer = f"Task executed, {username}." if success else "I encountered an error."
            ActionExecuted = True
            break

    # 3. Image Generation
    if is_image and not ActionExecuted:
        img_query = next(i for i in Decision if "generate" in i)
        img_data_path = BASE_DIR / "Frontend" / "Files" / "ImageGeneration.data"
        with open(img_data_path, "w") as f:
            f.write(f"{img_query},True")
        
        
        script_path = BASE_DIR / "Backend" / "ImageGeneratic.py"
        subprocess.Popen([sys.executable, str(script_path)], shell=False)
        
        Answer = f"Starting image generation for: {img_query.replace('generate', '').strip()}."
        ActionExecuted = True

    # 4. Chat / Search Logic
    if not ActionExecuted:
        if is_realtime:
            set_assis("Searching...")
            clean_q = next(i.replace("realtime", "").strip() for i in Decision if "realtime" in i)
            Answer = realtimesearchengine(clean_q)
        else:
            set_assis("Thinking...")
            Answer = chatbot(Query)

    # 5. Save and Show
    chat_data = ReadChatLogJson()
    chat_data.append({"role": "user", "content": Query})
    chat_data.append({"role": "assistant", "content": Answer})
    
    log_path = BASE_DIR / "Data" / "Chatlog.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(chat_data, f, indent=4)

    ChatLogIntegration()
    ShowChatsOnGUI()
    set_assis("Available ...")
    
    await Text_to_speech(Answer)
    return Answer

# --- Threading Management ---
def BackgroundLoop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    InitialExecution()

    while True:
        if getmicrophonedata() == "True":
            # SetMicrophoneStatus is set to False in STT.py usually, 
            # but we force it here to be safe
            loop.run_until_complete(MainExecution())
        else:
            time.sleep(0.3)

if __name__ == "__main__":
    try:
        # Start Backend Logic
        backend_thread = threading.Thread(target=BackgroundLoop, daemon=True)
        backend_thread.start()

        # Start Frontend GUI (Main Thread)
        launch_gui()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Finalizing shutdown...")
        try:
            driver.quit()
        except:
            pass
        stop_assistant_chrome()
        sys.exit()