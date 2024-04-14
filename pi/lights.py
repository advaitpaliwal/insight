from rpi_ws281x import PixelStrip, Color
import time

# Configuration (make these numbers larger if unsure)
LED_COUNT = 300          # Number of LED pixels (set this higher than you expect your strip to be)
LED_PIN = 18             # GPIO pin connected to the pixels (must support PWM)
LED_FREQ_HZ = 800000     # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10             # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 20      # Set to a low brightness
LED_INVERT = False       # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0          # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Initialize the library (strip)
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

def test_leds(strip):
    """Light up each LED in sequence to find the last one."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(255, 0, 0))  # Red color
        strip.show()
        time.sleep(0.1)
        strip.setPixelColor(i, Color(0, 0, 0))  # Turn off after testing
        strip.show()

try:
    test_leds(strip)
except KeyboardInterrupt:
    # Turn off all LEDs
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
