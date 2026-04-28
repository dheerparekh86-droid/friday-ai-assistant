import webbrowser
import subprocess
import os
import time
from datetime import datetime

def get_time():
    return datetime.now().strftime("Time is %I:%M %p Boss.")

def get_date():
    return datetime.now().strftime("Today is %B %d, %Y Boss.")
# ─────────────────────────────────────────
# BASIC WEB OPENERS
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


# ─────────────────────────────────────────
# APP OPENERS
# ─────────────────────────────────────────
def open_vscode():
    try:
        subprocess.Popen("code")  # works if VS Code is in PATH
        return "Opening VS Code Boss."
    except:
        return "VS Code not found Boss."


# ─────────────────────────────────────────
# FIRE UP MODE 🔥
# ─────────────────────────────────────────
def fire_up(speak_func=None):
    """
    Opens coding environment:
    VS Code + Claude + YouTube
    """

    if speak_func:
        speak_func("Diving into code Boss.")

    # Open VS Code
    subprocess.Popen(r"C:\Users\DHEER PAREKH\AppData\Local\Programs\Microsoft VS Code\Code.exe")

    # Small delay for smoother experience
    time.sleep(1)

    # Open Claude
    webbrowser.open("https://claude.ai")

    time.sleep(1)

    # Open YouTube (for coding/music)
    webbrowser.open("https://www.youtube.com")

    return "Environment ready Boss."


# ─────────────────────────────────────────
# GENERIC WEBSITE
# ─────────────────────────────────────────
def open_website(url):
    webbrowser.open(url)
    return f"Opening {url}"
import wikipedia

def quick_fact(topic):
    try:
        summary = wikipedia.summary(topic, sentences=2)
        return summary
    except:
        return f"I couldn't find clear info on {topic}, Boss."
import pyautogui
import time
import os

def take_screenshot():
    try:
        # Create screenshots folder if not exists
        folder = "screenshots"
        if not os.path.exists(folder):
            os.makedirs(folder)

        filename = f"{folder}/screenshot_{int(time.time())}.png"

        screenshot = pyautogui.screenshot()
        screenshot.save(filename)

        return f"Screenshot saved Boss."
    
    except Exception as e:
        return f"Failed to take screenshot Boss. {e}"
import webbrowser

def google_search(query):
    try:
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        return f"Searching for {query} Boss."
    except Exception as e:
        return f"Search failed Boss. {e}"