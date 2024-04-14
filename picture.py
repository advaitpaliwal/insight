# try:
#     from picamera2 import Picamera2
# except:
#     pass
# from time import sleep


# def take_picture(filepath: str):
#     """Take a picture using the Picamera2 library and save it to the provided file path."""
#     print("Taking picture...")

#     picam2 = Picamera2()

#     # Create a camera configuration for preview
#     camera_config = picam2.create_preview_configuration()

#     # Configure the camera with the preview configuration
#     picam2.configure(camera_config)

#     # Start the camera preview using DRM for non-GUI
#     picam2.start_preview(Preview.QTGL)

#     # Start the camera
#     picam2.start()

#     # Wait for 2 seconds to allow the camera sensor to adjust
#     sleep(2)

#     # Capture an image and save it as filepath"
#     picam2.capture_file(filepath)

#     # Stop the camera
#     picam2.stop()

#     print(f"Picture taken and saved as {filepath}")
#     return f"Picture taken and saved as {filepath}"


import cv2
from time import sleep
from text_to_speech import speak


def take_picture(filepath: str):
    """Take a picture using the specified camera and save it to the provided file path."""
    speak("Alright, I'm taking a picture now.")
    print("Taking picture...")
    cap = cv2.VideoCapture(0)
    sleep(2)
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        cap.release()
        return None

    cv2.imwrite(filepath, frame)
    print(f"Picture taken and saved as {filepath}")
    cap.release()
    speak("Got it! I've taken picture and saved it.")
    return f"Picture taken and saved as {filepath}"
