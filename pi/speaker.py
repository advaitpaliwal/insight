import pygame
import time
from gpiozero import PWMLED
from signal import pause

# Initialize pygame mixer
pygame.mixer.init()

# Load the WAV file
sound = pygame.mixer.Sound('output.wav')

# Set up PWM pin for speaker on GPIO 18 (which corresponds to physical pin 12)
speaker_pwm = PWMLED(18)

# Function to play sound
def play_sound():
    speaker_pwm.value = 0.5  # Set a fixed duty cycle for the PWM signal
    sound.play()

# Main function
if __name__ == "__main__":
    print("Playing sound...")
    play_sound()

    # Wait until the sound is finished playing
    while pygame.mixer.get_busy():
        time.sleep(0.1)

    speaker_pwm.off()
    print("Finished playing.")
