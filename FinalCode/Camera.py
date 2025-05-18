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
	try:
		while True:
			frame = picam2.capture_array()
			frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
			yield frame_bgr
	except generatorExit:
		pass
	except KeyboardInterrupt:
		print("interrupted by user")
	finally:
		print("stopping cam")
		picam2.stop()

def producer(frame_q, stop_evt):
	print("producer started")
	try:
		for frame in capture_frames():
			if stop_evt.is_set():
				break
			if not frame_q.full():
				frame_q.put(frame)
	except Exception as e:
		print(f"[Producer] Error : {e}")
	print("producer finished")



