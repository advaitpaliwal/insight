import pvcheetah
import pyaudio
import struct
from config import PICOVOICE_ACCESS_KEY
from text_to_speech import speak
import random

listening_phrases = [
    "Yes, how can I assist?",
    "I'm here, what do you need?",
    "Listening, go ahead!",
    "How can I help you today?",
    "I'm ready, what's up?",
    "What can I do for you?",
    "Go ahead, I'm all ears!",
    "Ready when you are!",
    "Yes, what would you like?",
    "How may I assist you today?"
]


def recognize_speech(endpoint_duration_sec=1.0):
    cheetah = None
    pa = None
    audio_stream = None

    try:
        cheetah = pvcheetah.create(
            access_key=PICOVOICE_ACCESS_KEY,
            endpoint_duration_sec=endpoint_duration_sec,
            enable_automatic_punctuation=True
        )
        print("One moment please...")
        pa = pyaudio.PyAudio()
        speak(random.choice(listening_phrases))
        print("Listening...")
        audio_stream = pa.open(
            rate=cheetah.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=cheetah.frame_length
        )
        partials = []
        while True:
            pcm = audio_stream.read(cheetah.frame_length)
            pcm = struct.unpack_from("h" * cheetah.frame_length, pcm)
            partial_transcript, is_endpoint = cheetah.process(pcm)
            partials.append(partial_transcript)
            print(f"Partial transcript: {''.join(partials)}", end="\r")
            if is_endpoint:
                break

        final_transcript = ''.join(partials) + cheetah.flush()
        print(f"\nRecognized: {final_transcript}")
        return final_transcript

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if cheetah is not None:
            cheetah.delete()
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()


if __name__ == "__main__":
    recognize_speech(endpoint_duration_sec=1.5)
