python -c "
import pyaudio, numpy as np
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
print('Clap now! Showing volume levels:')
for i in range(50):
    data = stream.read(1024, exception_on_overflow=False)
    vol = int(np.max(np.abs(np.frombuffer(data, dtype=np.int16))))
    print(f'Volume: {vol}', '█' * (vol // 500))
stream.close(); pa.terminate()
"