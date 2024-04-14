import pvporcupine
import pyaudio
import struct
import speech_recognition as sr
from src.config import PICOVOICE_ACCESS_KEY
from src.service import chat
from src.text_to_speech import speak
from src.recognize_speech import recognize_speech


def main():
    porcupine = None
    pa = None
    audio_stream = None

    try:
        # Initialize Porcupine with the wake word
        porcupine = pvporcupine.create(
            access_key=PICOVOICE_ACCESS_KEY, keywords=["hey google"])

        # Setup PyAudio to capture audio input
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        print("Listening for 'Hey Google'...")

        # Main loop to process audio and check for wake words
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            # Check if the wake word was detected
            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                print("Wake word detected! Listening for your command...")
                user_input = recognize_speech()
                print(f"User said: {user_input}")
                # Use the recognizer to listen for the next command
                response = chat.send_message(user_input)
                speak(response.text)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Clean up resources
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()


if __name__ == "__main__":
    main()
