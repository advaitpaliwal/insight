from google.cloud import texttospeech
import os
import pygame
from time import sleep
import tempfile


def speak(text: str):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_file.write(response.audio_content)
        temp_file_path = temp_file.name

    print(f'Audio content written to temporary file: {temp_file_path}')

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the temporary audio file
    pygame.mixer.music.load(temp_file_path)

    # Play the audio file
    pygame.mixer.music.play()

    # Wait for the music to play completely
    while pygame.mixer.music.get_busy():
        sleep(0.5)

    # Remove the temporary file
    os.remove(temp_file_path)


if __name__ == "__main__":
    speak("Hello, how are you?")
