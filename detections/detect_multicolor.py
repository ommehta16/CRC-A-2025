import cv2
import numpy as np
from detect_rect import find_rectangles

# HSV ranges for red (split range), yellow, and green
RED_RANGES = [
    ([0, 150,  60], [10, 255, 255]),
    ([170,150,  60], [180,255,255])
]
COLOR_RANGES = {
    'yellow': ([20, 100, 100], [30, 255, 255]),
    'green':  ([60, 120,  60], [70, 255, 255]),
}

def detect_colored_rectangles(frame_bgr):
    """
    Returns a list of dicts: [{'color': name, 'position':(x,y,w,h)}, ...]
    """
    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
    detections = []

    # Detect red (wrap-around HSV)
    for low, high in RED_RANGES:
        mask = cv2.inRange(hsv, np.array(low), np.array(high))
        kernel = np.ones((5,5), np.uint8)
        clean  = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        for (x, y, w, h) in find_rectangles(clean):
            detections.append({'color': 'red', 'position': (x, y, w, h)})

    # Detect yellow and green
    for name, (low, high) in COLOR_RANGES.items():
        mask = cv2.inRange(hsv, np.array(low), np.array(high))
        kernel = np.ones((5,5), np.uint8)
        clean  = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        for (x, y, w, h) in find_rectangles(clean):
            detections.append({'color': name, 'position': (x, y, w, h)})

    return detections
