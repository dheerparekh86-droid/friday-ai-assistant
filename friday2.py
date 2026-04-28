import os
import asyncio
import threading
import speech_recognition as sr

from dotenv import load_dotenv
from groq import Groq
import edge_tts
import pygame
import skills2

# ─────────────────────────
# LOAD ENV (CRITICAL)
# ─────────────────────────
load_dotenv()

# ─────────────────────────
# GROQ CLIENT (ONLY ONCE)
# ─────────────────────────
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ─────────────────────────
# CONFIG
# ─────────────────────────
VOICE = "en-US-JennyNeural"
AUDIO_FILE = "friday_voice.mp3"
friday_awake = False

# ─────────────────────────
# MEMORY
# ─────────────────────────
conversation_history = [
    {
        "role": "system",
        "content": "You are Friday, a smart AI assistant. Call user Boss. Keep replies short and confident."
    }
]

# ─────────────────────────
# SPEAK
# ─────────────────────────
async def _gen_audio(text):
    tts = edge_tts.Communicate(text, voice=VOICE)
    await tts.save(AUDIO_FILE)

def speak(text):
    print(f"\n🔊 Friday: {text}\n")
    try:
        asyncio.run(_gen_audio(text))
        pygame.mixer.init()
        pygame.mixer.music.load(AUDIO_FILE)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.quit()
    except Exception as e:
        print("Audio error:", e)

# ─────────────────────────
# LISTEN
# ─────────────────────────
def listen():
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 1.0
    recognizer.energy_threshold = 300

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.3)
        print("🎙️ Listening...")
        try:
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=12)
            text = recognizer.recognize_google(audio)
            print(f"👤 Boss: {text}")
            return text.lower().strip()
        except:
            return None

# ─────────────────────────
# AI BRAIN (GROQ)
# ─────────────────────────
def think(text):
    global conversation_history

    conversation_history.append({
        "role": "user",
        "content": text
    })

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=conversation_history,
            max_tokens=200
        )

        reply = response.choices[0].message.content

        conversation_history.append({
            "role": "assistant",
            "content": reply
        })

        return reply

    except Exception as e:
        return f"Error Boss: {e}"

# ─────────────────────────
# COMMAND ROUTER (FIXED)
# ─────────────────────────
def handle_command(text):

    # TIME / DATE
    if "time" in text:
        return skills2.get_time()

    if "date" in text or "today" in text:
        return skills2.get_date()

    # YOUTUBE
    if "youtube" in text:
        query = text.replace("youtube", "").strip()
        return skills2.open_youtube(query)

    # GOOGLE SEARCH (FIXED)
    if "search" in text or "google" in text:
        query = text.replace("search for", "").replace("search", "").replace("google", "").strip()

        if query:
            return skills2.google_search(query)
        else:
            return "What should I search Boss?"

    # OPEN APPS
    if "open" in text:
        app = text.replace("open", "").strip()

        if "chatgpt" in app:
            return skills2.open_chatgpt()

        if "claude" in app:
            return skills2.open_claude()

        return skills2.open_app(app)

    # SCREENSHOT
    if "screenshot" in text:
        return skills2.take_screenshot()

    # FIRE MODE
    if "fire up" in text or text == "fire":
        return skills2.fire_up(speak)

    # DEFAULT → AI
    return think(text)

# ─────────────────────────
# WAKE SYSTEM
# ─────────────────────────
def wait_wake(event):
    while not event.is_set():
        text = listen()
        if text and "friday" in text:
            print("✅ Wake word detected")
            event.set()

def sleep_mode():
    global friday_awake
    friday_awake = False

    e = threading.Event()
    threading.Thread(target=wait_wake, args=(e,), daemon=True).start()

    print("💤 Waiting for wake word...")
    e.wait()
    friday_awake = True

# ─────────────────────────
# MAIN LOOP
# ─────────────────────────
def main():
    print("=== FRIDAY READY ===")

    while True:
        sleep_mode()
        speak("I'm here Boss.")

        while friday_awake:
            text = listen()

            if not text:
                continue

            if "exit friday" in text:
                speak("Shutting down Boss.")
                return

            if "sleep" in text:
                speak("Going to sleep Boss.")
                break

            response = handle_command(text)
            speak(response)

# ─────────────────────────
# START
# ─────────────────────────
if __name__ == "__main__":
    main()

