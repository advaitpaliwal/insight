import pygame
import time


def play_wav(file_path):
    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the WAV file
    pygame.mixer.music.load(file_path)

    # Play the WAV file
    pygame.mixer.music.play()

    # Wait for the music to play completely
    while pygame.mixer.music.get_busy():
        time.sleep(1)  # Wait for the audio to finish playing


# Path to your WAV file
wav_file = 'output.mp3'

# Play the WAV file
play_wav(wav_file)
