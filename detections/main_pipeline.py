import time
from multiprocessing import Process, Queue, Event

from capture import capture_frames
from detect_multicolor import detect_colored_rectangles

def producer(frame_q, stop_evt):
    for frame in capture_frames():
        if stop_evt.is_set():
            break
        frame_q.put(frame)

def detector(frame_q, info_q, stop_evt):
    while not stop_evt.is_set():
        frame = frame_q.get()
        dets  = detect_colored_rectangles(frame)
        if dets:
            info_q.put(dets)

def consumer(info_q, stop_evt):
    while not stop_evt.is_set():
        dets = info_q.get()
        print("Detected:", dets)

if __name__ == "__main__":
    frame_queue = Queue(maxsize=5)
    info_queue  = Queue(maxsize=5)
    stop_event  = Event()

    procs = [
        Process(target=producer, args=(frame_queue, stop_event)),
        Process(target=detector, args=(frame_queue, info_queue, stop_event)),
        Process(target=consumer, args=(info_queue, stop_event)),
    ]
    for p in procs:
        p.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        stop_event.set()
        for p in procs:
            p.join()
