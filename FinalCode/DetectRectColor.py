import cv2
import numpy as np
import multiprocessing as mp

MIN_AREA = 1000

RED_RANGES = [
    ([0, 100,  40], [10, 255, 255]),
    ([170, 100, 40], [180, 255, 255])
]

COLOR_RANGES = {
    'yellow': ([20,  80,  80], [35, 255, 255]),
    'green':  ([40,  50,  40], [90, 255, 255])  # Wider range for green
}




def find_rectangles(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rects = []
    for cnt in contours:
        peri   = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
        area   = cv2.contourArea(approx)
        if len(approx) == 4 and area > MIN_AREA:
            x, y, w, h = cv2.boundingRect(approx)
            rects.append((x, y, w, h))
    return rects

def detect_colored_rectangles(frame_bgr):
    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
    detections = []

    for low, high in RED_RANGES:
        mask = cv2.inRange(hsv, np.array(low), np.array(high))
        kernel = np.ones((5,5), np.uint8)
        clean  = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        for (x, y, w, h) in find_rectangles(clean):
            detections.append({'color': 'red', 'position': (x, y, w, h)})

    for name, (low, high) in COLOR_RANGES.items():
        mask = cv2.inRange(hsv, np.array(low), np.array(high))
        kernel = np.ones((5,5), np.uint8)
        clean  = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        for (x, y, w, h) in find_rectangles(clean):
            detections.append({'color': name, 'position': (x, y, w, h)})

    return detections

def detector(frame_q:mp.Queue, annotated_q:mp.Queue, stop_evt):
    while not stop_evt.is_set():
        if frame_q.empty():
            continue
        frame = frame_q.get()
        detections = detect_colored_rectangles(frame)

        for det in detections:
            x, y, w, h = det['position']
            color = det['color']
            color_bgr = {
                'red': (0, 0, 255),
                'yellow': (0, 255, 255),
                'green': (0, 255, 0)
            }[color]
            if w > 10 and h > 10: annotated_q.put((x,y,w,h,color))
            cv2.rectangle(frame, (x, y), (x + w, y + h), color_bgr, 2)
            cv2.putText(frame, color, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color_bgr, 2)

        if not annotated_q.full():
            annotated_q.put(frame)

def consumer(annotated_q:mp.Queue, color_queue:mp.Queue, stop_evt):
    while not stop_evt.is_set():
        if annotated_q.empty():
            continue
        frame = annotated_q.get()
        if type(frame) == tuple:
            color_queue.put(frame)
            continue
        cv2.imshow("Detected Rectangles", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_evt.set()
            break
    cv2.destroyAllWindows()