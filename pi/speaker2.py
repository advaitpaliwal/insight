import time
from gpiozero import PWMOutputDevice
from scipy.io import wavfile

# Define PWM device on GPIO pin 18
pwm_pin = PWMOutputDevice(18)

# Load .wav file
sample_rate, data = wavfile.read('path/to/your/soundfile.wav')

# Normalizing data for PWM (0-1 scale)
normalized_data = data / max(abs(data))

# Playing the sound
for sample in normalized_data:
    pwm_pin.value = (sample + 1) / 2  # Convert -1->1 range into 0->1
    time.sleep(1 / sample_rate)

# Stop PWM output
pwm_pin.close()
