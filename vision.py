import pyautogui
import cv2
import numpy as np
from PIL import Image
import tempfile
from groq import Groq
import base64
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ─────────────────────────────────────────
# TAKE SCREENSHOT
# ─────────────────────────────────────────
def capture_screen():
    screenshot = pyautogui.screenshot()
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    screenshot.save(temp_file.name)
    return temp_file.name

# ─────────────────────────────────────────
# IMAGE → BASE64
# ─────────────────────────────────────────
def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ─────────────────────────────────────────
# AI VISION ANALYSIS
# ─────────────────────────────────────────
def analyze_screen(image_path, instruction):
    image_base64 = encode_image(image_path)

    response = client.chat.completions.create(
        model="llama-3.2-90b-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": instruction},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/png;base64,{image_base64}"
                    }
                ]
            }
        ]
    )

    return response.choices[0].message.content

# ─────────────────────────────────────────
# CLICK USING AI
# ─────────────────────────────────────────
def click_element(description):
    path = capture_screen()

    prompt = f"""
    Find the coordinates (x,y) of: {description}
    Return ONLY in format: x,y
    """

    result = analyze_screen(path, prompt)

    try:
        x, y = map(int, result.strip().split(","))
        pyautogui.click(x, y)
        return f"Clicked {description}"
    except:
        return "Couldn't find element Boss."