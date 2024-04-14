import cv2
from time import sleep


def take_picture(camera_index=0):
    """Take a picture using the specified camera and save it as picture.jpg."""
    print("Taking picture...")
    cap = cv2.VideoCapture(camera_index)
    sleep(2)
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        cap.release()
        return None

    cv2.imwrite('picture.jpg', frame)
    print("Picture taken and saved as picture.jpg")
    cap.release()
    return "Picture taken and saved as picture.jpg"
