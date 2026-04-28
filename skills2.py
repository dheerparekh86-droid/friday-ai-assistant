import webbrowser
import subprocess
import os
import time
from datetime import datetime
import pyautogui
import wikipedia

# ─────────────────────────────────────────
# TIME & DATE
# ─────────────────────────────────────────
def get_time():
    return datetime.now().strftime("Time is %I:%M %p Boss.")

def get_date():
    return datetime.now().strftime("Today is %B %d, %Y Boss.")


# ─────────────────────────────────────────
# WEB FUNCTIONS
# ─────────────────────────────────────────
def open_youtube(query=None):
    if query:
        url = f"https://www.youtube.com/results?search_query={query}"
    else:
        url = "https://www.youtube.com"

    webbrowser.open(url)
    return "Opening YouTube Boss."


def open_chatgpt():
    webbrowser.open("https://chat.openai.com")
    return "Opening ChatGPT Boss."


def open_claude():
    webbrowser.open("https://claude.ai")
    return "Opening Claude Boss."


def google_search(query):
    try:
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Searching for {query} Boss."
    except Exception as e:
        return f"Search failed Boss. {e}"


def open_website(url):
    webbrowser.open(url)
    return f"Opening {url} Boss."


# ─────────────────────────────────────────
# APP CONTROL
# ─────────────────────────────────────────
APP_PATHS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
    "cmd": "cmd.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "vs code": r"C:\Users\DHEER PAREKH\AppData\Local\Programs\Microsoft VS Code\Code.exe"
}


def open_app(app):
    app = app.lower()

    if app in APP_PATHS:
        try:
            subprocess.Popen(APP_PATHS[app])
            return f"Opening {app} Boss."
        except:
            return f"Couldn't open {app} Boss."

    # fallback
    try:
        subprocess.Popen(app)
        return f"Opening {app} Boss."
    except:
        return f"I couldn't find {app} Boss."


def open_vscode():
    return open_app("vs code")


# ─────────────────────────────────────────
# FIRE UP MODE 🔥
# ─────────────────────────────────────────
def fire_up(speak_func=None):
    if speak_func:
        speak_func("Diving into code Boss.")

    # VS Code
    try:
        subprocess.Popen("code")
    except:
        try:
            subprocess.Popen(APP_PATHS["vs code"])
        except:
            print("⚠️ VS Code not found")

    time.sleep(1)

    # Claude
    webbrowser.open("https://claude.ai")

    time.sleep(1)

    # YouTube
    webbrowser.open("https://www.youtube.com")

    return "Environment ready Boss."


# ─────────────────────────────────────────
# SCREENSHOT
# ─────────────────────────────────────────
def take_screenshot():
    try:
        folder = "screenshots"
        os.makedirs(folder, exist_ok=True)

        filename = os.path.join(folder, f"screenshot_{int(time.time())}.png")

        screenshot = pyautogui.screenshot()
        screenshot.save(filename)

        return "Screenshot saved Boss."

    except Exception as e:
        return f"Screenshot failed Boss. {e}"


# ─────────────────────────────────────────
# QUICK FACT
# ─────────────────────────────────────────
def quick_fact(topic):
    try:
        summary = wikipedia.summary(topic, sentences=2)
        return summary
    except:
        return f"I couldn't find clear info on {topic}, Boss."