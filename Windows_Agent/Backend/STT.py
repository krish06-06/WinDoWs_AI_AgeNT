import os
import time
import psutil
import mtranslate as mt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values

# Load environment variables
env_vars = dotenv_values(".env")
inputLAN = env_vars.get("InputLanguage", "en")

def stop_assistant_chrome():
    """Kills only the headless chrome to free the mic."""
    for proc in psutil.process_iter(['name', 'cmdline']):
        try:
            if "chrome" in proc.info['name'].lower() and "--headless" in str(proc.info['cmdline']):
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

# HTML code for web
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

# File Setup
data_dir = "Data"
os.makedirs(data_dir, exist_ok=True)
html_path = os.path.join(data_dir, "Voice.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(HtmlCode)

# SELENIUM SETUP 
chrome_options = Options()
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
Link = f"file:///{os.path.abspath(html_path)}"

def QueryModify(Query):
    new_query = Query.lower().strip()
    if not new_query: return ""
    question_words = ["who", "what", "when", "where", "why", "how", "which"]
    if any(new_query.startswith(word) for word in question_words):
        new_query = new_query.rstrip(".?!") + "?"
    else:
        new_query = new_query.rstrip(".?!") + "."
    return new_query.capitalize()

def universaltranslator(Text):
    try: return mt.translate(Text, "en", "auto").capitalize()
    except: return Text

#Speech Recog function in genral
"""def SpeechRecognition():
    #Listens and returns text using the working logic.
    driver.get(Link)
    driver.find_element(By.ID, "start").click()

    while True:
        try:
            # Reverted to simple .text check
            Text = driver.find_element(By.ID, "output").text.strip()
            
            if Text:
                # Click end to trigger the manualStop flag in JS
                driver.find_element(By.ID, "end").click()
                
                if "en" in inputLAN.lower():
                    return QueryModify(Text)
                else:
                    return QueryModify(universaltranslator(Text))
            
            time.sleep(0.4)
        except Exception as e:
            # Silently retry on minor Selenium errors
            time.sleep(0.5)"""
#if main throws thread killing error
def SpeechRecognition():
    """Starts recognition with a retry logic to prevent StaleElement errors."""
    driver.get(Link)
    
    # Give the page a split second to load
    time.sleep(0.5) 

    
    for _ in range(3): 
        try:
            start_btn = driver.find_element(By.ID, "start")
            start_btn.click()
            break
        except Exception:
            time.sleep(0.2)
            continue

    while True:
        try:
            Text = driver.find_element(By.ID, "output").text.strip()
            
            if Text:
                # Use a JS click to be safer against stale elements
                driver.execute_script("document.getElementById('end').click();")
                
                if "en" in inputLAN.lower():
                    return QueryModify(Text)
                else:
                    return QueryModify(universaltranslator(Text))
            
            time.sleep(0.4)
        except Exception:
            
            time.sleep(0.5)

def final_speech_recog():
    try:
        while True:
            print("Listening...")
            result = SpeechRecognition()
            print(f"Recognized: {result}")
    except KeyboardInterrupt:
        print("Shutting Down......")
        pass
    finally:
        driver.quit()
        stop_assistant_chrome()


if __name__ == "__main__":
    final_speech_recog()