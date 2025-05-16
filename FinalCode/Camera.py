from picamera2 import Picamera2
import cv2
import time

def capture_frames(width=640, height=360):
    """
    Generator that yields BGR frames from Picamera2 with continuous autofocus.
    """
    picam2 = Picamera2()
    config = picam2.create_video_configuration(main={"size": (width, height)})
    picam2.configure(config)
    picam2.set_controls({"AfMode": 2})  # Continuous autofocus
    picam2.start()
    time.sleep(2)

    while True:
        frame = picam2.capture_array()
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        yield frame_bgr

def producer(frame_q, stop_evt):
    for frame in capture_frames():
        if stop_evt.is_set():
            break
        if not frame_q.full():
            frame_q.put(frame)



