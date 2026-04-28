import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize model
model = genai.GenerativeModel("gemini-1.5-flash")

conversation_history = []

def think(text):
    global conversation_history

    conversation_history.append({"role": "user", "parts": [text]})

    try:
        response = model.generate_content(conversation_history)

        reply = response.text.strip()

        conversation_history.append({"role": "model", "parts": [reply]})

        return reply

    except Exception as e:
        return f"I ran into an issue Boss. {e}"