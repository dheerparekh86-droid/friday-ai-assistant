import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

chat = client.chat.completions.create(
  model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": "You are Friday, an advanced AI assistant built for your Boss. You are confident, intelligent, and occasionally witty. You always address the user as 'Boss'. You speak like the AI assistant from Iron Man."
        },
        {
            "role": "user",
            "content": "Introduce yourself."
        }
    ]
)

print(chat.choices[0].message.content)