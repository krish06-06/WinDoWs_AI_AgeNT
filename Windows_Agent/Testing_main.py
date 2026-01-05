#Testing main.py for Debugging Purpose or Teting New Freatures

import asyncio
from Backend.Model import FirstlayerDMM
from Backend.Chatbot import chatbot
from Backend.Realtimesearchengine import realtimesearchengine
from Backend.Automation import Automation
from Backend.TTS import Text_to_speech
from Frontend.gui import launch_gui

async def MainExecution(query):
    """
    Processes a single query through the AI pipeline.
    This is called by the GUI whenever text is submitted or voice is recognized.
    """
    if not query:
        return ""

   
    decisions = FirstlayerDMM(query)
    
    final_response = ""

    for task in decisions:
        # Handle Exit
        if "exit" in task:
            response = "Goodbye! I am shutting down."
            await Text_to_speech(response)
            return response

        # Handle Automation (Open/Close/Play)
        elif any(action in task for action in ["open", "close", "play"]):
            await Automation([task])
            response = f"Sure, performing the {task} task for you."
            await Text_to_speech(response)
            final_response += response

        # Handle Real-time Search
        elif "realtime" in task:
            search_query = task.replace("realtime", "").strip()
            response = realtimesearchengine(search_query)
            await Text_to_speech(response)
            final_response += response

        # Handle General Conversation
        elif "general" in task:
            chat_query = task.replace("general", "").strip()
            response = chatbot(chat_query)
            await Text_to_speech(response)
            final_response += response
            
    return final_response

if __name__ == "__main__":
    # To start the assistant, we simply launch the GUI.
    # The GUI will handle calling MainExecution internally.
    launch_gui()