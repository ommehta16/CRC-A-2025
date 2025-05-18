from multiprocessing import Process, Queue, Event, set_start_method
from Camera import producer
from DetectRectColor import detector
import time


frame_queue     = Queue(maxsize=5)
annotated_queue = Queue(maxsize=5)
color_queue = Queue()
stop_event      = Event()
procs = [
    Process(target=producer, args=(frame_queue, stop_event)),
    Process(target=detector, args=(frame_queue, color_queue, stop_event)),
    # Process(target=consumer, args=(annotated_queue, color_queue, stop_event)),
]
try:
    for p in procs: p.start()
except Exception as e:
    for p in procs:
        if p.is_alive():
            p.join(timeout=2) # Wait for processes to finish
        if p.is_alive():
            print(f"Process {p.name} did not terminate, killing.")
            p.kill() # Force kill if join times out
        print("All processes joined.")
