import numpy as np
import sounddevice as sd
import webrtcvad
import collections
import scipy.signal
from faster_whisper import WhisperModel

# ─────────────────────────────────────────
# CONFIG (TUNED)
# ─────────────────────────────────────────
RATE = 16000
FRAME_DURATION = 30
FRAME_SIZE = int(RATE * FRAME_DURATION / 1000)

VAD_MODE = 1          # LESS sensitive (important)
SILENCE_LIMIT = 40    # more speaking time

model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)

# ─────────────────────────────────────────
# FILTER
# ─────────────────────────────────────────
def is_valid(text, confidence, audio_len):
    if not text:
        return False

    if len(text) < 3:
        return False

    if len(text.split()) < 2:
        return False

    if audio_len < RATE * 1.2:   # ignore tiny audio
        return False

    if confidence < -1.0:
        return False

    bad = ["thank you", "thanks", "you", "uh", "hmm"]
    if text in bad:
        return False

    return True

# ─────────────────────────────────────────
# LISTEN
# ─────────────────────────────────────────
def listen():
    print("🎙️ Listening (stable)...")

    vad = webrtcvad.Vad(VAD_MODE)

    ring_buffer = collections.deque(maxlen=40)  # bigger buffer
    audio_buffer = []

    speaking = False

    stream = sd.InputStream(
        samplerate=RATE,
        channels=1,
        dtype="int16"
    )

    stream.start()

    try:
        while True:
            frame, _ = stream.read(FRAME_SIZE)
            frame_bytes = frame.tobytes()

            is_speech = vad.is_speech(frame_bytes, RATE)

            if not speaking:
                ring_buffer.append(frame)

                if is_speech:
                    speaking = True
                    audio_buffer.extend(ring_buffer)
                    ring_buffer.clear()

            else:
                audio_buffer.append(frame)

                if not is_speech:
                    ring_buffer.append(frame)

                    # allow pauses
                    if len(ring_buffer) > SILENCE_LIMIT:
                        if len(audio_buffer) < RATE * 1.5:
                            continue
                        break
                else:
                    ring_buffer.clear()

    finally:
        stream.stop()
        stream.close()

    if not audio_buffer:
        return ""

    # ─────────────────────────────────────────
    # PROCESS
    # ─────────────────────────────────────────
    audio = np.concatenate(audio_buffer, axis=0).flatten().astype(np.float32)

    if np.max(np.abs(audio)) > 0:
        audio = audio / np.max(np.abs(audio))

    audio = audio * 1.5  # boost mic
    audio = scipy.signal.lfilter([1], [1, -0.97], audio)
    audio = audio.astype(np.float32)

    print("⚙️ Processing...")

    segments, _ = model.transcribe(audio, beam_size=5)

    text = ""
    confidence = 0

    for seg in segments:
        text += seg.text
        confidence += seg.avg_logprob

    text = text.strip().lower()

    if not is_valid(text, confidence, len(audio)):
        return ""

    print(f"👤 Boss: {text}")
    return text