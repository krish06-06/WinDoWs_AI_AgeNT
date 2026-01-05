import google.generativeai as genai
from rich import print
import os
import sys
from dotenv import dotenv_values
import time 
from pathlib import Path  


base_path = Path(__file__).resolve().parent.parent
env_path = base_path / ".env"
#print(env_path) 

# Check if .env exists to avoid "bastard" crashes
if not env_path.exists():
    print(f"⚠️ Warning: .env not found at {env_path}")

env_vars = dotenv_values(str(env_path))
#print(env_vars)  # Debugging line to check loaded env vars
GeminiAPIKey = env_vars.get("GEMINI_API_KEY")
#print(GeminiAPIKey)
genai.configure(api_key=GeminiAPIKey)
# -------------------------------------






# Preamble
preamble = """
You are a helpful AI Assistant. Your task is to classify user queries into specific categories.
*** You must NOT answer queries, only classify them. ***

-> Respond with 'general (query)' if it is a standard conversational question.
-> Respond with 'realtime (query)' if it requires current information (news, weather, time).
-> Respond with 'open (app/website)' if the user wants to launch something.
-> Respond with 'close (app/website)' if the user wants to exit something.
-> Respond with 'generate (prompt)' for image generation requests.
-> Respond with 'google search (topic)' for Google searches.
-> Respond with 'exit' if the user wants to end the session.

*** If a query asks for multiple actions, respond with a comma-separated list. ***
"""

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash", # Updated to latest stable flash u can use 2.5 too
    system_instruction=preamble
)

#ADD MORE FUNCTIONS IF U WANT 
funcs = [
    "exit", "general", "realtime", "open", "close","generate", "google search"
]

# Reduced Chat history 
ChatHistory = [
    {"role": "User", "message": "hello"},
    {"role": "Chatbot", "message": "general hello"},
    {"role": "User", "message": "what time is it?"},
    {"role": "Chatbot", "message": "realtime what time is it?"},
    {"role": "User", "message": "open browser and check the news"},
    {"role": "Chatbot", "message": "open browser, realtime check the news"}
]

def FirstlayerDMM(prompt: str, max_retries=3):
    messages = []

    # Convert ChatHistory to Gemini format
    for chat in ChatHistory:
        role = "user" if chat["role"] == "User" else "model"
        messages.append({"role": role, "parts": [chat["message"]]})

    messages.append({"role": "user", "parts": [prompt]})

    for attempt in range(max_retries):
        try:
            response = model.generate_content(
                messages,
                generation_config=genai.GenerationConfig(
                    temperature=0.3,
                    top_p=0.9,
                    max_output_tokens=128
                )
            )

            response_text = response.text.strip().replace("\n", ", ")
            response_list = [i.strip() for i in response_text.split(",")]

            classified_responses = [
                task for task in response_list
                if any(task.startswith(func) for func in funcs)
            ]

            if classified_responses:
                return classified_responses
            else:
                print(f"⚠️ Empty response, retrying ({attempt+1}/{max_retries})...")
                time.sleep(4)

        except Exception as e:
            print(f"❌ Error: {e}. Retrying ({attempt+1}/{max_retries})...")
            time.sleep(3)

    return ["general (query)"]

if __name__ == "__main__":
    while True:
        user_input = input(">>> ")
        decision = FirstlayerDMM(user_input)
        print(f"Decision: {decision}")