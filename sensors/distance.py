#https://docs.sunfounder.com/projects/umsk/en/latest/05_raspberry_pi/pi_lesson21_vl53l0x.html

#use pololu!!!
'''
sudo apt-get install python3-pip
pip3 install git+https://github.com/pololu/vl53l0x-python.git

'''

import time
import RPi.GPIO as GPIO
from vl53l0x import VL53L0X

# Use BOARD numbering
GPIO.setmode(GPIO.BOARD)
XSHUT_1 = 11  # GPIO17
XSHUT_2 = 13  # GPIO27
GPIO.setup(XSHUT_1, GPIO.OUT)
GPIO.setup(XSHUT_2, GPIO.OUT)

# Power-cycle both sensors
GPIO.output(XSHUT_1, GPIO.LOW)
GPIO.output(XSHUT_2, GPIO.LOW)
time.sleep(0.1)

GPIO.output(XSHUT_1, GPIO.HIGH)
time.sleep(0.1)
sensor1 = VL53L0X()
sensor1.open()
sensor1.change_address(0x30)

GPIO.output(XSHUT_2, GPIO.HIGH)
time.sleep(0.1)
sensor2 = VL53L0X()
sensor2.open()

# Start ranging
sensor1.start_ranging(VL53L0X.VL53L0X_HIGH_ACCURACY_MODE)
sensor2.start_ranging(VL53L0X.VL53L0X_HIGH_ACCURACY_MODE)

# Wall-following settings
target_distance = 200  # mm (adjust based on your desired distance from wall)
tolerance = 10         # mm (acceptable wiggle room)
check_interval = 0.1   # seconds

print(f"Target wall distance: {target_distance} mm ± {tolerance} mm")

try:
    while True:
        sideDis = sensor1.get_distance()  # sensor1 is side-facing toward the wall
        if sideDis > (target_distance + 800):
            sideTrend = 0#"no side wall"
        elif sideDis < (target_distance - tolerance):
            sideTrend = 1# "Too Close – Steer Away"
        elif sideDis > (target_distance + tolerance):
            sideTrend = 2#"Too Far – Steer Toward Wall"
        else:
            trend = 3#"On Track"
        
        print(f"Distance: {d} mm | Status: {trend}")
        frontDis = sensor2.get_distance()  # sensor2 is side-facing toward front
        if frontDis < (500):
            frontTrend = 1 #blocked in front
        else:
            frontTrend = 0
        if sideTrend==0:
            pass #left turn around corner, this is a pivot, and then move
        elif sideTrend!=0 and frontTrend==1:
            pass #right turn before corner, this is a pivot in place
        elif sideTrend==1:
            pass #slight turn
        elif sideTrend==2:
            pass #slight turn
        else sideTrend==3:
            pass #go forward

        time.sleep(check_interval)

except KeyboardInterrupt:
    print("Stopping...")

finally:
    sensor1.stop_ranging()
    sensor2.stop_ranging()
    GPIO.cleanup()
