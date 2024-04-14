from picamera2 import Picamera2, Preview
import time

# Create an instance of the PiCamera2 class
picam2 = Picamera2()

# Create a camera configuration for preview
camera_config = picam2.create_preview_configuration()

# Configure the camera with the preview configuration
picam2.configure(camera_config)

# Start the camera preview using DRM for non-GUI
picam2.start_preview(Preview.QTGL)

# Start the camera
picam2.start()

# Wait for 2 seconds to allow the camera sensor to adjust
time.sleep(2)

# Capture an image and save it as "test.jpg"
picam2.capture_file("test.jpg")
