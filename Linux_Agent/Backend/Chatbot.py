from groq import Groq
from json import load, dump
import datetime
from dotenv import dotenv_values
from pathlib import Path  # <--- Added for cross-platform paths


base_path = Path(__file__).resolve().parent.parent
env_path = base_path / ".env"
data_dir = base_path / "Data"
log_file = data_dir / "chatlog.json"

# Create 'Data' directory if it doesn't exist (prevents crash on first run)
data_dir.mkdir(exist_ok=True)
# -------------------------

# Loading environment variables
env_vars = dotenv_values(str(env_path))

# Fallbacks
Username = env_vars.get("Username", "User")
Assistantname = env_vars.get("assis_name", "Assistant")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

messages = []

#Preamble
system = f"""You are a helpful and polite AI Assistant named {Assistantname}. 
You provide accurate information and assist the user with their queries.
Always reply in English and maintain a professional tone.
"""

system_chatbot = [
    {"role": "system", "content": system}
]

# Ensure data directory exists or handle chatlog logic
try:
    with open(r"Data\chatlog.json", "r") as f:
        messages = load(f)
except (FileNotFoundError, ValueError):
    
    messages = []

def realtimeinformation():
    current_date_time = datetime.datetime.now()
    day = current_date_time.strftime("%A")
    date = current_date_time.strftime("%d")
    month = current_date_time.strftime("%B")
    year = current_date_time.strftime("%Y")
    hour = current_date_time.strftime("%H")
    minute = current_date_time.strftime("%M")
    second = current_date_time.strftime("%S")

    data = f"System Context (Real-time):\n"
    data += f"Day: {day}, Date: {date} {month} {year}\n"
    data += f"Time: {hour}:{minute}:{second}\n"

    return data

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer

def chatbot(Query):
    try:
        # Load latest history
        try:
            with open(log_file, "r") as f:
                current_messages = load(f)
        except:
            current_messages = []

        
        current_messages.append({"role": "user", "content": Query})

        
        real_time_message = {"role": "system", "content": realtimeinformation()}

        
        messages_for_completion = system_chatbot + [real_time_message] + current_messages

        # API call with the llama model
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",   #You can change llama model here
            messages=messages_for_completion,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        Answer = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                Answer += chunk.choices[0].delta.content

        Answer = Answer.replace("</s>", "")
        Answer = AnswerModifier(Answer)

        # Append assistant's response to history
        current_messages.append({"role": "assistant", "content": Answer})

        # Save to chatlog
        with open(log_file, "w") as f:
            dump(current_messages, f, indent=4)

        return Answer 
    except Exception as e1:
        print(f"Error: {e1}")
        return "I encountered an error. Please check your configuration."

if __name__ == "__main__":
    while True:
        user_input = input("Enter Your Question: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        print(f"{Assistantname}: {chatbot(user_input)}")