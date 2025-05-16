import RPi.GPIO as GPIO
'''
from picamera2 import Picamera2

picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()

picam2.capture_file("image.jpg")

picam2.stop()
'''

import time
import board
import adafruit_vl53l0x

# Use BCM mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define XSHUT pins (BCM)
XSHUT_1 = 17
XSHUT_2 = 27

GPIO.setup(XSHUT_1, GPIO.OUT)
GPIO.setup(XSHUT_2, GPIO.OUT)

# Turn off both sensors
GPIO.output(XSHUT_1, GPIO.LOW)
GPIO.output(XSHUT_2, GPIO.LOW)
time.sleep(0.5)

# Initialize I2C
i2c = board.I2C()

# Turn on first sensor only
GPIO.output(XSHUT_1, GPIO.HIGH)
time.sleep(0.5)
tof1 = adafruit_vl53l0x.VL53L0X(i2c)

tof1.set_address(0x30)

# Turn on second sensor
GPIO.output(XSHUT_2, GPIO.HIGH)
time.sleep(0.5)
tof2 = adafruit_vl53l0x.VL53L0X(i2c)
tof2.set_address(0x31)

# Read both sensors
try:
    while True:
        d1 = tof1.range
        d2 = tof2.range
        print(f"Distance 1: {d1} mm, Distance 2: {d2} mm")
        time.sleep(0.3)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("GPIO cleaned up.")




