import os
import requests
import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
import skills

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

VOICE = "en-US-JennyNeural"
AUDIO_FILE = "friday.mp3"

conversation_history = [
    {
        "role": "system",
        "content": """You are Friday, an advanced AI assistant — confident, intelligent, and witty.
Always address the user as 'Boss'.
Keep responses concise — 1 to 3 sentences unless asked for detail.
You can control the laptop and perform tasks."""
    }
]

# ─────────────────────────────────────────
def speak(text):
    """Convert text to speech using Edge TTS (free Microsoft neural voice)."""
    import asyncio
    import edge_tts
    import pygame

    print(f"\n🔊 Friday: {text}\n")

    async def _speak():
        communicate = edge_tts.Communicate(text, voice="en-US-AriaNeural")
        await communicate.save("friday_speech.mp3")

    asyncio.run(_speak())

    # Play the audio
    pygame.mixer.init()
    pygame.mixer.music.load("friday_speech.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()
# ─────────────────────────────────────────
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("🎙️ Listening...")
        try:
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=12)
            text = recognizer.recognize_google(audio)
            print(f"👤 Boss: {text}")
            return text.lower()
        except:
            return None

# ─────────────────────────────────────────
def handle_command(text):
    """Check if the command matches a skill before sending to AI."""

    # TIME & DATE
    if "time" in text:
        return skills.get_time()
    if "date" in text or "today" in text:
        return skills.get_date()

    # YOUTUBE
    if "youtube" in text:
        query = text.replace("open youtube", "").replace("play", "").replace("on youtube", "").replace("youtube", "").strip()
        return skills.open_youtube(query if query else None)

    # MUSIC
    if "play music" in text or "play song" in text or ("play" in text and "music" in text):
        query = text.replace("play music", "").replace("play song", "").replace("play", "").replace("music", "").strip()
        return skills.play_music(query if query else "top hits")

    # GOOGLE SEARCH
    if "search" in text or "google" in text:
        query = text.replace("search for", "").replace("search", "").replace("google", "").strip()
        return skills.google_search(query)

    # OPEN WEBSITES
    if "open" in text and any(site in text for site in ["instagram", "twitter", "facebook", "gmail", "netflix", "reddit", "github"]):
        for site in ["instagram", "twitter", "facebook", "gmail", "netflix", "reddit", "github"]:
            if site in text:
                return skills.open_website(site + ".com")

    # OPEN APPS
    if "open" in text:
        for app in ["notepad", "calculator", "paint", "task manager", "file explorer", "word", "excel", "chrome", "spotify", "vs code"]:
            if app in text:
                return skills.open_app(app)

    # SCREENSHOT
    if "screenshot" in text:
        return skills.take_screenshot()

    # WEATHER
    if "weather" in text:
        city = "Nagpur"
        for word in text.replace("weather", "").replace("in", "").split():
            if len(word) > 2:
                city = word
                break
        return skills.get_weather(city)

    # LOCK PC
    if "lock" in text and ("pc" in text or "computer" in text or "screen" in text):
        return skills.lock_pc()

    # SHUTDOWN
    if "confirm shutdown" in text:
        return skills.confirm_shutdown()
    if "shutdown" in text or "shut down" in text:
        return skills.shutdown_pc()

    # WIKIPEDIA
    if "what is" in text or "who is" in text or "tell me about" in text:
        topic = text.replace("what is", "").replace("who is", "").replace("tell me about", "").strip()
        return skills.quick_fact(topic)
    if "youtube" in text:
     return skills.open_youtube()

    if "chatgpt" in text:
     return skills.open_chatgpt()

    if "claude" in text:
     return skills.open_claude()

    if "vs code" in text:
     return skills.open_vscode()

    if "fire up" in text:
     return skills.fire_up(speak)

    # DEFAULT — send to AI brain
    return think(text)

# ─────────────────────────────────────────
def think(user_input):
    conversation_history.append({"role": "user", "content": user_input})
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=conversation_history,
        max_tokens=200
    )
    reply = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": reply})
    return reply

# ─────────────────────────────────────────
def main():
    print("=" * 50)
    print("       F.R.I.D.A.Y  —  Online")
    print("=" * 50)
    print()
    print("Try saying:")
    print("  • 'What time is it'")
    print("  • 'Play Believer on YouTube'")
    print("  • 'Open Instagram'")
    print("  • 'Search for Tesla news'")
    print("  • 'What is black hole'")
    print("  • 'Take a screenshot'")
    print("  • 'What's the weather'")
    print("  • 'Open calculator'")
    print()

    speak("Good day Boss. HOW can i assist you today")

    while True:
        user_input = listen()
        if not user_input:
            continue

        if any(word in user_input for word in ["goodbye", "exit", "shut down friday", "bye friday"]):
            speak("understood boss good bye have a great day")
            break

        response = handle_command(user_input)
        speak(response)

if __name__ == "__main__":
    main()