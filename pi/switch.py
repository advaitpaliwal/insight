import pyaudio
import numpy as np
import time
import subprocess

# Initialize PyAudio
pa = pyaudio.PyAudio()

# Constants for audio stream
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1              # Single channel for microphone
RATE = 44100              # Sampling rate
CHUNK = 1024              # Number of audio samples per frame


def open_mic_stream():
    stream = pa.open(format=FORMAT,
                     channels=CHANNELS,
                     rate=RATE,
                     input=True,
                     frames_per_buffer=CHUNK)
    return stream


def audio_callback():
    stream = open_mic_stream()
    try:
        while True:
            data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
            audio_level = np.abs(np.max(data) - np.min(data))
            threshold = 1000

            if audio_level > threshold:
                print("Audio input detected")
                time.sleep(0.2)
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()


while True:
    audio_callback()
