import os

# ===== CONFIG =====
CURRENT_DIR = os.getcwd()
TEMP_DIR = os.path.join(CURRENT_DIR, "Frontend", "Files")
GRAPHICS_DIR = os.path.join(CURRENT_DIR, "Frontend", "Graphics")
RESPONSES_FILE = os.path.join(TEMP_DIR, "Responses.data")
MIC_FILE = os.path.join(TEMP_DIR, "Mic.data")
STATUS_FILE = os.path.join(TEMP_DIR, "Status.data")
#print(CURRENT_DIR)
#print(TEMP_DIR)



# ===== FILE PATH HELPERS =====
def temp_dir_path(filename):
    """Return full path for a file in TEMP_DIR."""
    return os.path.join(TEMP_DIR, filename)

def graphic_dir(filename):
    """Return full path for a file in GRAPHICS_DIR."""
    return os.path.join(GRAPHICS_DIR, filename)


# ===== ASSISTANT STATUS =====
def set_assis(status):
    """Write assistant status to Status.data"""
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        f.write(status)

def get_assis():
    """Read assistant status from Status.data"""
    if not os.path.exists(STATUS_FILE):
        return ""
    with open(STATUS_FILE, "r", encoding="utf-8") as f:
        return f.read()


# ===== MICROPHONE CONTROL =====
def Setmicrophonestatus(status):
    """Write mic status ('True'/'False') to Mic.data"""
    with open(MIC_FILE, "w", encoding="utf-8") as f:
        f.write(status)

def getmicrophonedata():
    """Read mic status from Mic.data"""
    if not os.path.exists(MIC_FILE):
        return "False"
    with open(MIC_FILE, "r", encoding="utf-8") as f:
        return f.read()


# ===== CHAT RESPONSE HELPERS =====
def showtexttoscreen(text):
    """Write assistant response to Responses.data"""
    with open(RESPONSES_FILE, "w", encoding="utf-8") as f:
        f.write(text)

def Answermodif(answer):
    """Remove empty lines from assistant answer"""
    lines = answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    return "\n".join(non_empty_lines)

def querymodif(query):
    """Format user query to proper punctuation"""
    new_query = query.lower().strip()
    question_words = [
        "who", "what", "when", "where", "why", "how", "which", "whom", "whose",
        "can", "could", "shall", "should", "will", "would", "may", "might", "must",
        "is", "are", "was", "were", "do", "does", "did", "has", "have", "had",
        "can you", "what's", "how's", "where's", "what is"
    ]
    if any(word + " " in new_query for word in question_words):
        if new_query[-1] not in ['?', '.', '!']:
            new_query += "?"
        else:
            new_query = new_query[:-1] + "?"
    else:
        if new_query[-1] not in ['?', '.', '!']:
            new_query += "."
        else:
            new_query = new_query[:-1] + "."
    return new_query.capitalize()


# ===== TEMP FILE CLEANUP =====
def clear_temp_files():
    """Clear all temp files to reduce lag at startup/shutdown"""
    files = [RESPONSES_FILE, MIC_FILE, STATUS_FILE]
    for f in files:
        if os.path.exists(f):
            with open(f, "w", encoding="utf-8") as file:
                file.write("")

