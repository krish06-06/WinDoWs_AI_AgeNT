from googlesearch import search
from groq import Groq
from json import load, dump
from dotenv import dotenv_values
import datetime
from ddgs import DDGS
from pathlib import Path 


base_path = Path(__file__).resolve().parent.parent
env_path = base_path / ".env"
data_dir = base_path / "Data"
log_file = data_dir / "chatlog.json"

# Create Data folder if missing
data_dir.mkdir(exist_ok=True)
# -------------------------

# Load environment variables using the absolute path
env_vars = dotenv_values(str(env_path))


Username = env_vars.get("Username", "User")
Assistantename = env_vars.get("assis_name", "Assistant")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

# preamble 
System = f"""You are a highly capable AI Assistant named {Assistantename}.
You have access to real-time search results to provide accurate and up-to-date information.
Maintain a professional tone and ensure clarity in your responses.
"""

# Initial chatbot memory
system_chatbot = [
    {"role": "system", "content": System},
    {"role": "user", "content": "Hi"},
    {"role": "assistant", "content": "Hello! I am ready to help you with real-time information. What would you like to know?"}
]

# Load previous chat log or create a new one
try:
    with open(log_file, "r") as f:
        messages = load(f)
except (FileNotFoundError, ValueError):
    messages = []

# Function to perform Search using DDGS
def googlesearch(query):
    with DDGS() as ddgs:
        # 
        results = list(ddgs.text(query, max_results=3))
    
    Answer = f"Web Search Results for '{query}':\n[Search Start]\n"
    
    if not results:
        Answer += "No immediate web results found."
    else:
        for i in results:
            Answer += f"Title: {i.get('title')}\nDescription: {i.get('body')}\n\n"

    Answer += "[Search End]"
    return Answer

# Function to get real-time date and time info
def information():
    current_date_time = datetime.datetime.now()
    return (
        f"Contextual Time/Date:\n"
        f"Day: {current_date_time.strftime('%A')}\n"
        f"Date: {current_date_time.strftime('%d %B %Y')}\n"
        f"Time: {current_date_time.strftime('%H:%M:%S')}\n"
    )

def AnswerModifier(Answer):
    return Answer.strip().replace("</s>", "")

# Main real-time search function
def realtimesearchengine(prompt):
    global system_chatbot, messages

    try:
        with open(log_file, "r") as f:
            messages = load(f)
    except:
        messages = []

    # Keep a concise history
    messages = messages[-5:] 

    
    messages.append({"role": "user", "content": prompt})
    
    
    search_data = googlesearch(prompt)

    
    current_system_context = [
        {"role": "system", "content": System},
        {"role": "system", "content": search_data},
        {"role": "system", "content": information()}
    ]

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant", #llma model
        messages=current_system_context + messages,
        max_tokens=1024,
        temperature=0.5, # Slightly lower temperature for more factual search responses
        top_p=1,
        stream=True,
        stop=None
    )

    Answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    Answer = AnswerModifier(Answer)

    # Save to chat log
    messages.append({"role": "assistant", "content": Answer})
    with open(log_file, "w") as f:
        dump(messages, f, indent=4)

    return Answer

if __name__ == "__main__":
    while True:
        prompt = input("Search Query: ")
        if prompt.lower() in ["exit", "quit"]:
            break
        print(f"\n{Assistantename}: {realtimesearchengine(prompt)}\n")

        