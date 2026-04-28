def speak(text):
    """Convert text to speech using Edge TTS (free Microsoft neural voice)."""
    import asyncio
    import edge_tts
    import pygame

    print(f"\n🔊 Friday: {text}\n")

    async def _speak():
        communicate = edge_tts.Communicate(text, voice="en-US-JennyNeural")
        await communicate.save("friday_speech.mp3")

    asyncio.run(_speak())

    # Play the audio
    pygame.mixer.init()
    pygame.mixer.music.load("friday_speech.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.quit()