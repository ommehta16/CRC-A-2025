if __name__ == "__main__":
    from multiprocessing import Process, Queue, Event, set_start_method
    import time

    try:
        set_start_method("spawn")  # Required for RPi/Picamera2
    except RuntimeError:
        pass

    frame_queue = Queue(maxsize=5)
    color_queue = Queue()
    stop_event = Event()

    procs = [
        Process(target=producer, args=(frame_queue, stop_event)),
        Process(target=detector, args=(frame_queue, color_queue, stop_event)),
    ]

    try:
        for p in procs:
            p.start()
        for p in procs:
            p.join()
    except KeyboardInterrupt:
        stop_event.set()
    finally:
        for p in procs:
            if p.is_alive():
                p.terminate()
        print("Processes terminated.")
