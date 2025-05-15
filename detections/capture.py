import cv2

def capture_frames(camera_index=0, width=640, height=480):
    """
    Generator that yields frames from the camera.
    """
    cap = cv2.VideoCapture(camera_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        yield frame

    cap.release()
