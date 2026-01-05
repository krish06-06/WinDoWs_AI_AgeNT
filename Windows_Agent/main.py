import os
import sys
import json
import time
import asyncio
import threading
import subprocess
import pygame
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
from Backend.STT import SpeechRecognition,stop_assistant_chrome,driver
from Backend.Chatbot import chatbot
from Backend.TTS import Text_to_speech

# --- Environment & Performance Setup ---
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
env_vars = dotenv_values(".env")
username = env_vars.get("Username", "User")
assis_name = env_vars.get("assis_name", "Assistant")



# Default values
Defaultmessage = f"{username}: Hello {assis_name}.\n{assis_name}: Welcome! I am online and ready to help."
Functions = ["open", "close","google search"] # Automation Functions if u add something in future you can change here as well as the logic in Automation.py 

# Chat Log Logic
def ReadChatLogJson():
    """Reads history from Data/ChatLog.json safely."""
    path = os.path.join("Data", "ChatLog.json")
    try:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data if data else [{"role": "assistant", "content": Defaultmessage}]
    except (FileNotFoundError, json.JSONDecodeError):
        return [{"role": "assistant", "content": Defaultmessage}]

def ChatLogIntegration():
    """Formats JSON chat history into a string for the GUI Database."""
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    for entry in json_data:
        role = entry["role"].lower()
        if role == "user":
            formatted_chatlog += f"{username}: {entry['content']}\n"
        else:
            formatted_chatlog += f"{assis_name}: {entry['content']}\n"
    
    with open(temp_dir_path('Database.data'), 'w', encoding='utf-8') as file:
        file.write(Answermodif(formatted_chatlog))

def ShowChatsOnGUI():
    """Syncs the internal Database.data with the visible Responses.data."""
    try:
        with open(temp_dir_path('Database.data'), "r", encoding="utf-8") as file:
            Data = file.read()
        if Data.strip():
            showtexttoscreen(Data)
    except Exception as e:
        print(f"GUI Sync Error: {e}")

# Initial Setup
def InitialExecution():
    Setmicrophonestatus("False")
    ChatLogIntegration()
    ShowChatsOnGUI()
    set_assis("Available ...")

# Core AI Logic
async def MainExecution(Query: str = None):
    """
    The heart of the AI. It takes a query, classifies it via DMM,
    triggers search, automation, or chat, and speaks the answer.
    """
    ActionExecuted = False
    Answer = ""

    # 1. Input Handling
    if Query is None:
        set_assis("Listening ...")
        Query = SpeechRecognition()
    
    # 2. Intent Classification (DMM)
    Decision = FirstlayerDMM(Query)
    
    # Clean up decision lists if model returns nested items
    Decision = [str(i) for i in (Decision if isinstance(Decision, list) else [Decision])]

    # 3. Task Sorting
    is_realtime = any(i.startswith("realtime") for i in Decision)
    is_general = any(i.startswith("general") for i in Decision)
    is_image = any("generate" in i for i in Decision)
    exit=any(i.startswith("exit") for i in Decision)
    

    
    # 4. Automation check
    for q in Decision:
        if any(q.startswith(f) for f in Functions):
            success = await Automation(Decision)
            Answer = f"Task executed, {username}." if success else "I encountered an error."
            ActionExecuted = True
            break

    # 5. Image Generation check
    if is_image and not ActionExecuted:
        img_query = next(i for i in Decision if "generate" in i)
        with open(os.path.join("Frontend", "Files", "ImageGeneration.data"), "w") as f:
            f.write(f"{img_query},True")
        subprocess.Popen(["python", os.path.join("Backend", "ImageGeneratic.py")], shell=False)
        Answer = f"Starting image generation for: {img_query.replace('generate', '')}."
        ActionExecuted = True

    # 6. Chat / Search Logic
    if not ActionExecuted:
        if is_realtime:
            set_assis("Searching...")
            clean_q = next(i.replace("realtime", "").strip() for i in Decision if "realtime" in i)
            Answer = realtimesearchengine(clean_q)
        elif is_general:
            set_assis("Thinking...")
            Answer = chatbot(Query)
        elif "exit" :
            response = "Goodbye! I am shutting down."
            await Text_to_speech(response)
            #Full shutdown process, if there is more external processes to shutdown u can make a function to use again and again if needed
            print("Finalizing shutdown...")
            driver.quit()
            stop_assistant_chrome 
            os._exit(0)
            return response  
        else :
            pass

    # 7. Save and Show
    chat_data = ReadChatLogJson()
    chat_data.append({"role": "user", "content": Query})
    chat_data.append({"role": "assistant", "content": Answer})
    
    with open(os.path.join("Data", "ChatLog.json"), "w", encoding="utf-8") as f:
        json.dump(chat_data, f, indent=4)

    ChatLogIntegration() # Update internal DB
    ShowChatsOnGUI()    # Update GUI Screen
    
    # 8. Speak the result
    await Text_to_speech(Answer)
    return Answer

# Threading Management
def BackgroundLoop():
    """Background thread that watches for the GUI to toggle the Microphone."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    InitialExecution()

    while True:
        if getmicrophonedata() == "True":
            # Reset mic status to avoid multiple triggers
            Setmicrophonestatus("False")
            loop.run_until_complete(MainExecution())
        else:
            time.sleep(0.3)


if __name__ == "__main__":
    try:
        
        gui_thread = threading.Thread(target=BackgroundLoop, daemon=True)
        gui_thread.start()

        launch_gui()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # THIS SECTION IS KEY:
        # It triggers when the GUI window is closed
        print("Finalizing shutdown...")
        driver.quit()
        stop_assistant_chrome # Call the specific cleanup from STT.py
        sys.exit()
