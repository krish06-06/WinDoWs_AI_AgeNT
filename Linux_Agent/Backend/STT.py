import os
import time
import psutil
import shutil  
import mtranslate as mt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pathlib import Path
from dotenv import load_dotenv


# Resolves paths relative to the project root
base_path = Path(__file__).resolve().parent.parent
env_path = base_path / ".env"
load_dotenv(env_path)
inputLAN = os.getenv("InputLanguage", "en")

def stop_assistant_chrome():
    """Clean up any lingering headless chrome processes."""
    for proc in psutil.process_iter(['name', 'cmdline']):
        try:
            if "chrome" in proc.info['name'].lower() and "--headless" in str(proc.info['cmdline']):
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass


HtmlCode = f'''<!DOCTYPE html>
<html lang="en">
<head><title>Speech Recognition</title></head>
<body>
    <button id="start" onclick="startRecognition()">Start</button>
    <button id="end" onclick="stopRecognition()">Stop</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;
        let manualStop = false;

        function startRecognition() {{
            manualStop = false;
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '{inputLAN}';
            recognition.continuous = true;

            recognition.onresult = function(event) {{
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript; 
            }};

            recognition.onend = function() {{ 
                if (!manualStop) {{ recognition.start(); }}
            }};
            recognition.start();
        }}

        function stopRecognition() {{
            manualStop = true;
            if(recognition) {{ recognition.stop(); }}
            output.innerHTML = "";
        }}
    </script>
</body>
</html>'''

# --- FILE SETUP ---
data_dir = base_path / "Data"
data_dir.mkdir(parents=True, exist_ok=True)
html_path = data_dir / "Voice.html"
with open(html_path, "w", encoding="utf-8") as f:
    f.write(HtmlCode)

# --- SELENIUM NIXOS FIX ---
chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream") # Bypasses Mic popup
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")


chrome_bin = shutil.which("google-chrome-stable") or shutil.which("google-chrome")
driver_bin = shutil.which("chromedriver")

if not driver_bin:
    raise RuntimeError("❌ Chromedriver not found! Please ensure you ran 'nix-shell'.")

if chrome_bin:
    chrome_options.binary_location = chrome_bin


service = Service(executable_path=driver_bin)

try:
    driver = webdriver.Chrome(service=service, options=chrome_options)
except Exception as e:
    print(f"⚠️ Service initialization error: {e}. Attempting fallback...")
    driver = webdriver.Chrome(options=chrome_options)

Link = f"file://{html_path.absolute()}"

# --- PROCESSING FUNCTIONS ---

def QueryModify(Query):
    """Clean up and format the recognized text."""
    new_query = Query.lower().strip()
    if not new_query: return ""
    question_words = ["who", "what", "when", "where", "why", "how", "which"]
    if any(new_query.startswith(word) for word in question_words):
        new_query = new_query.rstrip(".?!") + "?"
    else:
        new_query = new_query.rstrip(".?!") + "."
    return new_query.capitalize()

def universaltranslator(Text):
    """Translate non-English input if necessary."""
    try: 
        return mt.translate(Text, "en", "auto").capitalize()
    except Exception: 
        return Text

def SpeechRecognition():
    """The main loop that interacts with the browser to get text."""
    driver.get(Link)
    time.sleep(0.5) 

    # Trigger the JS start function
    try:
        driver.execute_script("document.getElementById('start').click();")
    except Exception as e:
        print(f"Error starting recognition: {e}")

    while True:
        try:
            output_element = driver.find_element(By.ID, "output")
            Text = output_element.text.strip()
            
            if Text:
                # Stop recognition and clear output for next run
                driver.execute_script("document.getElementById('end').click();")
                
                if "en" in inputLAN.lower():
                    return QueryModify(Text)
                else:
                    return QueryModify(universaltranslator(Text))
            
            time.sleep(0.4)
        except Exception:
            time.sleep(0.5)

def final_speech_recog():
    """Continuous listening loop."""
    try:
        while True:
            print("🎤 Listening...")
            result = SpeechRecognition()
            print(f"💡 Recognized: {result}")
    except KeyboardInterrupt:
        print("\n👋 Shutting Down Speech Engine...")
    finally:
        driver.quit()
        stop_assistant_chrome()

if __name__ == "__main__":
    final_speech_recog()