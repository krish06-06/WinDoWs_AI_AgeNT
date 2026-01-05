# Backend/Automation.py
from webbrowser import open as webopen
#from pywhatkit import search, playonyt
from dotenv import load_dotenv
from pathlib import Path
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import subprocess
import os
import asyncio
#import requests
#import time


base_path = Path(__file__).resolve().parent.parent

# Define the path to .env and the Data folder correctly
env_path = base_path / ".env"
data_dir = base_path / "Data"
chatlog_path = data_dir / "chatlog.json"

data_dir.mkdir(parents=True, exist_ok=True)


load_dotenv(env_path) 

# Now we pull it from the environment
Username= os.getenv("Username", "User")
Assistantname=os.getenv("assis_name", "Assistant")
GroqAPIKey=os.getenv("GroqAPIKey")

# Debugging print 
if GroqAPIKey:
    print(f"✅ Key Loaded from env path")
else:
    print(f"❌ Key still NONE. Check if .env exists at: {env_path}")

client=Groq(api_key= GroqAPIKey)

useragent=os.getenv("user_agent")



#----------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------

messages = []
systemchatbot = [{
    "role": "system",
    "content": f"Hello, I am {Username}, you're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems, etc."
}]

Professional_responses = [
    f"Your satisfaction is my priority {Username}; feel free to reach out if there's anything else I can help you with.",
    f"I am at your service {Username} for any additional questions or support you may need - don't hesitate to ask."
]

# Google HTML parsers
def extract_links(html):
    if html is None:
        return []
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all("a", {'jsname': 'UWckNb'})
    return [link.get('href') for link in links if link.get('href') and link.get('href').startswith("http")]

def search_google(query, sess):
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": useragent}
    response = sess.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print("[red]Failed to retrieve search results.[/red]")
        return None

# Open app logic (system + external)

def Openapp(app):
    app = app.lower().strip()

    linux_apps = {
        "firefox": ["firefox"],
        "brave": ["brave"],
        "browser": ["brave"],
        "code": ["code"],
        "vscode": ["code"],
        "terminal": ["kitty"],      # change if needed
        "files": ["nautilus"],
        "calculator": ["gnome-calculator"],
    }

    websites = {
        "youtube": "https://www.youtube.com",
        "gmail": "https://mail.google.com",
        "instagram": "https://www.instagram.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://twitter.com",
        "reddit": "https://www.reddit.com",
    }

    try:
        # 1️⃣ Known apps
        if app in linux_apps:
            subprocess.Popen(linux_apps[app])
            return True

        # 2️⃣ Known websites
        if app in websites:
            webopen(websites[app])
            return True

        # 3️⃣ Try raw binary
        subprocess.Popen([app])
        return True

    except FileNotFoundError:
        # 4️⃣ Final fallback → Google search
        webopen(f"https://www.google.com/search?q={app}")
        return False


def closeapp(app):
    app = app.lower().strip()
    try:
        subprocess.run(["pkill", "-f", app])
        return True
    except Exception as e:
        print(f"Failed to close app: {e}")
        return False

# System commands Its not Added yet just have to change the model preamble to add system commands

def system(command):
    match command:
        case "mute":
            subprocess.run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "toggle"])
        case "volume up":
            subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "+5%"])
        case "volume down":
            subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "-5%"])
        case "shutdown pc":
            subprocess.run(["shutdown", "now"])
        case "restart pc":
            subprocess.run(["reboot"])
        case _:
            print("Unknown system command")
    return True


# Google search via browser
def Googlesearch(query):
    webopen(f"https://www.google.com/search?q={query}")
    return True

#Future additions: Play on YouTube juts gave an idea to add ,If u want to add this freature chnage Model handelling throuhgh preamble
def playonyt(query):
    webopen(f"https://www.youtube.com/results?search_query={query}")
    return True

# Async command execution
async def translate_and_execute(commands: list[str]):
    funcs = []

    for command in commands:
        command = command.lower()
        if command.startswith("open "):
            fun = asyncio.to_thread(Openapp, command.removeprefix("open "))
            funcs.append(fun)
        elif command.startswith("close "):
            fun = asyncio.to_thread(closeapp, command.removeprefix("close "))
            funcs.append(fun)
        elif command.startswith("play "):
            fun = asyncio.to_thread(playonyt, command.removeprefix("play "))
            funcs.append(fun)
        elif command.startswith("google search "):
            fun = asyncio.to_thread(Googlesearch, command.removeprefix("google search "))
            funcs.append(fun)
        elif command.startswith("system "):
            fun = asyncio.to_thread(system, command.removeprefix("system "))
            funcs.append(fun)
        else:
            print(f"[yellow]No function found for:[/yellow] {command}")

    results = await asyncio.gather(*funcs)
    for result in results:
        yield result

# Master automation
async def Automation(commands: list[str]):
    async for result in translate_and_execute(commands):
        pass
    return True

# Example usage (testing)
if __name__ == "__main__":
    
    while(True):
        choice = input("press 1 for openapp 2 for closeapp 3 for system\n")

        if choice == "1":
         query = input(">>> ")
         Openapp(query)

        elif choice == "2":
         query = input(">>> ")
         closeapp(query)

        elif choice == "3":
         query = input(">>> ")
         system(query)

        else:
         print("Invalid choice")

