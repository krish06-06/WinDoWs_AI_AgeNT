import pygame
import random
import asyncio
import edge_tts
import os
import textwrap
import time
from dotenv import load_dotenv
from pathlib import Path


base_path = Path(__file__).resolve().parent.parent
env_path = base_path / ".env"
speech_file = base_path / "Data" / "speech.mp3"

# Ensure Data directory exists
speech_file.parent.mkdir(parents=True, exist_ok=True)

# Load environment variables
load_dotenv(env_path)
AssistantVoice = os.getenv("AssistantVoice", "en-US-AndrewNeural")

# Initialize PyGame Mixer
pygame.init()
pygame.mixer.init()

async def TextToAudioFile(text):
    """Converts text to an mp3 file using Edge TTS."""
    
    # On Linux, we must ensure the mixer releases the file before deleting
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
        pygame.mixer.music.unload() 

    try:
        if speech_file.exists():
            os.remove(str(speech_file))
    except Exception as e:
        print(f"File status (Non-critical): {e}")

    communicate = edge_tts.Communicate(text, AssistantVoice, rate="+0%")
    await communicate.save(str(speech_file))

async def TTS(text, func=lambda r=None: True):
    """Plays the generated audio file."""
    if not text.strip():
        return

    try:
        await TextToAudioFile(text)

        # Reload mixer to ensure it hooks into the current NixOS audio sink
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            
        pygame.mixer.music.load(str(speech_file))
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
        pygame.mixer.music.unload() 

def update_chat_screen(text):
    print(f"\n[Assistant]: {text}")

async def Text_to_speech(text, func=lambda r=None: True):
    if not text.strip():
        return

    responses = [
        "I've displayed the full details on the screen for you.",
        "The complete information is available in the chat log.",
        "Please refer to the chat screen for the full text.",
        "The rest of the result is printed on your screen."
    ]

    if len(text) >= 300:
        wrapped_text = textwrap.wrap(text, width=300)
        first_part = wrapped_text[0]
        update_chat_screen(text)
        await TTS(f"{first_part}. {random.choice(responses)}", func)
    else:
        update_chat_screen(text)
        await TTS(text, func)

if __name__ == "__main__":
    async def main():
        print("TTS Module active (Cross-Platform). Type 'exit' to stop.")
        while True:
            text = input("Text to speak: ")
            if text.lower() == "exit":
                break
            await Text_to_speech(text)

    asyncio.run(main())