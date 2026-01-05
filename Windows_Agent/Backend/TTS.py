import pygame
import random
import asyncio
import edge_tts
import os
import textwrap
import time
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice", "en-US-AndrewNeural")

# Initialize PyGame
pygame.init()
pygame.mixer.init()

async def TextToAudioFile(text):
    """Converts text to an mp3 file using Edge TTS."""
    file_path = r"Data\speech.mp3"

    # Ensure the Data directory exists
    if not os.path.exists("Data"):
        os.makedirs("Data")

    
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    time.sleep(0.1)

    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"File status: {e}")

    pygame.mixer.init()

    communicate = edge_tts.Communicate(text, AssistantVoice, rate="+0%")
    await communicate.save(file_path)

async def TTS(text, func=lambda r=None: True):
    """Plays the generated audio file."""
    if not text.strip():
        return

    try:
        await TextToAudioFile(text)

        pygame.mixer.init()
        pygame.mixer.music.load(r"Data\speech.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.event.pump()
            if func() is False:
                break
            await asyncio.sleep(0.1)

    except Exception as e:
        print(f"TTS Playback Error: {e}")
    finally:
        func(False)
        pygame.mixer.music.stop()

def update_chat_screen(text):
    """Placeholder for UI updates."""
    print(f"\n[Assistant]: {text}")

async def Text_to_speech(text, func=lambda r=None: True):
    """Handles logic for long text and triggers speech."""
    if not text.strip():
        return

    # Generic responses for long text
    responses = [
        "I've displayed the full details on the screen for you.",
        "The complete information is available in the chat log.",
        "Please refer to the chat screen for the full text.",
        "The rest of the result is printed on your screen."
    ]

    
    if len(text) >= 250:
        wrapped_text = textwrap.wrap(text, width=250)
        first_part = wrapped_text[0]
        update_chat_screen(text) # Show full text in UI
        # Speak only the first part + a redirect message
        await TTS(f"{first_part}. {random.choice(responses)}", func)
    else:
        update_chat_screen(text)
        await TTS(text, func)

if __name__ == "__main__":
    async def main():
        print("TTS Module active. Type 'exit' to stop.")
        while True:
            text = input("Text to speak: ")
            if text.lower() == "exit":
                break
            await Text_to_speech(text)

    asyncio.run(main())