'''
The algorithim at its core, as pseudocode for now
'''
import time
from multiprocessing import Process, Queue, Event, set_start_method
from Camera import producer
from DetectRectColor import detector, consumer

'''
#everything should go in a try finally, with cleanup processes in the except keyboard interrupt
if __name__ == "__main__":
    #initialize everything, camera, pins, processes etc
    #run through ALL sensors
    #if camera sees something:
        #turn on lights, dispense, disable this function until a certain distance is traveled
    #if camera sees nothing:
        #is there anything significant on the color sensor OR frontfacing distance? if so, react
        #react to sideways wall distance
    #move
    #add movement to mapping, loop
'''

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



