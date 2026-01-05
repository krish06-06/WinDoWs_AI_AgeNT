import os
from pathlib import Path


# This finds the actual root of your project regardless of where you run the script from
BASE_DIR = Path(__file__).resolve().parent.parent
TEMP_DIR = BASE_DIR / "Frontend" / "Files"
GRAPHICS_DIR = BASE_DIR / "Frontend" / "Graphics"

# Ensure directories exist
TEMP_DIR.mkdir(parents=True, exist_ok=True)

RESPONSES_FILE = str(TEMP_DIR / "Responses.data")
MIC_FILE = str(TEMP_DIR / "Mic.data")
STATUS_FILE = str(TEMP_DIR / "Status.data")

# ===== FILE PATH HELPERS =====
def temp_dir_path(filename):
    return str(TEMP_DIR / filename)

def graphic_dir(filename):
    return str(GRAPHICS_DIR / filename)

# ===== ASSISTANT STATUS =====
def set_assis(status):
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        f.write(str(status))

def get_assis():
    if not os.path.exists(STATUS_FILE):
        return ""
    with open(STATUS_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()

# ===== MICROPHONE CONTROL =====
def Setmicrophonestatus(status):
    """Write mic status ('True'/'False') to Mic.data"""
    with open(MIC_FILE, "w", encoding="utf-8") as f:
        # We ensure it's always title-case 'True' or 'False'
        f.write(str(status).capitalize())

def getmicrophonedata():
    """Read mic status from Mic.data"""
    if not os.path.exists(MIC_FILE):
        return "False"
    with open(MIC_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()

# ===== CHAT RESPONSE HELPERS =====
def showtexttoscreen(text):
    with open(RESPONSES_FILE, "w", encoding="utf-8") as f:
        f.write(text)

def Answermodif(answer):
    """Clean up lines and strip whitespace"""
    return "\n".join([line.strip() for line in answer.split("\n") if line.strip()])

def querymodif(query):
    """Enhanced punctuation logic"""
    new_query = query.lower().strip()
    if not new_query: return ""

    question_words = [
        "who", "what", "when", "where", "why", "how", "which", "whom", "whose",
        "can", "could", "shall", "should", "will", "would", "is", "are", "do", "does"
    ]
    
    # Check if it's a question
    is_question = any(new_query.startswith(word) for word in question_words) or \
                  any(phrase in new_query for phrase in ["what's", "how's", "is it"])

    # Clean existing punctuation
    new_query = new_query.rstrip(".?!")

    if is_question:
        return new_query.capitalize() + "?"
    else:
        return new_query.capitalize() + "."

# ===== TEMP FILE CLEANUP =====
def clear_temp_files():
    """Clear all temp files. Useful for fresh starts."""
    for file_path in [RESPONSES_FILE, MIC_FILE, STATUS_FILE]:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write("")
        except Exception:
            pass