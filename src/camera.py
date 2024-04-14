from picamera2 import Picamera2
from time import sleep


def take_picture(filepath: str):
    """Take a picture using the Picamera2 library and save it to the provided file path."""
    print("Taking picture...")

    # Create an instance of the Picamera2 class
    picam2 = Picamera2()

    # Create a camera configuration for preview
    camera_config = picam2.create_preview_configuration()

    # Configure the camera with the preview configuration
    picam2.configure(camera_config)

    # Start the camera
    picam2.start()

    # Wait for 2 seconds to allow the camera sensor to adjust
    sleep(2)

    # Capture an image and save it to the specified file path
    picam2.capture_file(filepath)

    # Stop the camera
    picam2.stop()

    print(f"Picture taken and saved as {filepath}")
    return f"Picture taken and saved as {filepath}"
