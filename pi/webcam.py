import cv2
from time import sleep


def take_picture(filepath: str):
    """Take a picture using the specified camera and save it to the provided file path."""
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
    return f"Picture taken and saved as {filepath}"


take_picture("test.jpg")
