# THIS IS ALL IN root main.py
# delete once you see this @PhantomFrenzy151

'''
The algorithim at its core, as pseudocode for now
'''
import time
from multiprocessing import Process, Queue, Event, set_start_method
from Camera import producer
from DetectRectColor import detector, consumer
'''
PLS PUT STUFF IN CRC-A-2025/main.py
plsplsplps

this way its like synced and all

the point of having git is that we don't need to version control with copies
dslafhjlsahjfkhdsakjhfkaj
'''
#everything should go in a try finally, with cleanup processes in the except keyboard interrupt

if __name__ == "__main__":
    
    set_start_method("spawn")  # Required for Picamera2 multiprocessing

    frame_queue     = Queue(maxsize=5)
    annotated_queue = Queue(maxsize=5)
    stop_event      = Event()

    procs = [
        Process(target=producer, args=(frame_queue, stop_event)),
        Process(target=detector, args=(frame_queue, annotated_queue, stop_event)),
        Process(target=consumer, args=(annotated_queue, stop_event)),
    ]

    for p in procs:
        p.start()

    try:
        while not stop_event.is_set():
            time.sleep(0.5)
    except KeyboardInterrupt:
        stop_event.set()
    finally:
        for p in procs:
            p.join()



