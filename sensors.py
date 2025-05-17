import RPi.GPIO as GPIO
import time
import math
import adafruit_vl53l0x
import adafruit_tcs34725
import board
import adafruit_lsm9ds0
import tkinter as tk

#test code
root = tk.Tk()
root.title("Live Color Reader")
canvas = tk.Canvas(root, width=300, height=300)
canvas.pack()

def rgb_to_hex(r, g, b):
	return "#{:02x}{:02x}{:02x}".format(r, g, b)

####

buttonPin = 21
ledPin = 26
xshut1_pin = 17
xshut2_pin = 27
tcs_power_pin = 4
hall1_pin = 10
hall2_pin = 9
ledState = GPIO.LOW

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.output(ledPin, ledState)

GPIO.setup(xshut1_pin, GPIO.OUT)
GPIO.setup(xshut2_pin, GPIO.OUT)
GPIO.setup(tcs_power_pin, GPIO.OUT)

GPIO.setup(hall1_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(hall2_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

i2c = board.I2C()

tof1 = None
tof2 = None
color_sensor = None
imu = None

def toggleLED():
	global ledState
	ledState = GPIO.LOW if ledState == GPIO.HIGH else GPIO.HIGH
	GPIO.output(ledPin, ledState)
	print("LED toggled")
def blink(cnt=1):
	for i in range(cnt):
		toggleLED()
		time.sleep(0.5)
		toggleLED()
		time.sleep(0.5)
			

def initialize_sensors():
	global tof1, tof2, color_sensor, imu

	GPIO.output(tcs_power_pin, GPIO.LOW)

	GPIO.output(xshut1_pin, GPIO.LOW)
	GPIO.output(xshut2_pin, GPIO.LOW)
	time.sleep(0.3)

	GPIO.output(xshut1_pin, GPIO.HIGH)
	time.sleep(0.3)
	tof1 = adafruit_vl53l0x.VL53L0X(i2c)
	tof1.set_address(0x30)

	GPIO.output(xshut2_pin, GPIO.HIGH)
	time.sleep(0.3)
	tof2 = adafruit_vl53l0x.VL53L0X(i2c)
	tof2.set_address(0x31)

	GPIO.output(tcs_power_pin, GPIO.HIGH)
	time.sleep(0.3)
	
	color_sensor = adafruit_tcs34725.TCS34725(i2c)
	color_sensor.integration_time=150
	color_sensor.gain = 60

	imu = adafruit_lsm9ds0.LSM9DS0_I2C(i2c)
	print("Sensors initialized")
	

def get_distances():
	if tof1 and tof2:
		d1 = tof1.range
		d2 = tof2.range
		print(f"Distance 1: {d1} mm, Distance 2: {d2} mm")
		return d1, d2
	else:
		print("ToF sensors not initialized.")
		return None, None

def get_color():
	if color_sensor:
		r, g, b = color_sensor.color_rgb_bytes
		print(f"Color: R={r}, G={g}, B={b}")
		### more test code
		color_hex = rgb_to_hex(r, g, b)
		canvas.configure(bg=color_hex)
		root.update()
		return r, g, b
	else:
		print("Color sensor not initialized.")
		return None

def get_accel():
	if imu:
		x,y,z = imu.acceleration
		print(f"Acceleration (m/s^2): ({x:0.3f},{y:0.3f},{z:0.3f})")
		return x, y, z
	else:
		print("IMU not initialized.")
		return None
		

'''
accel_offset = [0.0, 0.0, 0.0]
accel_offset_initialized = False
'''
def get_pitch():
	'''
	global accel_offset, accel_offset_initialized
	ax,ay,az=get_accel()
	# On first call, capture the current reading as "level baseline"
	if not accel_offset_initialized:
		accel_offset = [ax, ay, az]
		accel_offset_initialized = True

	# Apply offset correction
	'''
	ax_corr = ax - 0#accel_offset[0]
	ay_corr = ay - 0#accel_offset[1]
	az_corr = az - 0#accel_offset[2]

	# Calculate pitch
	pitch_rad = math.atan2(-ax_corr, math.sqrt(ay_corr ** 2 + az_corr ** 2))
	pitch_deg = math.degrees(pitch_rad)
	print(pitch_deg)
	return pitch_deg





def get_gyro():
	if imu:
		x,y,z = imu.gyro
		print(f"Magnetometer (gauss): ({x:0.3f},{y:0.3f},{z:0.3f})")		
		return x, y, z
	else:
		print("IMU not initialized.")
		return None




def get_mag(): ###technically it can also do temp but we don't care
	global mag_min, mag_max
	if imu:
		x,y,z = imu.magnetic
		#print(f"Magnetometer (gauss): ({x:0.3f},{y:0.3f},{z:0.3f})")		
		return x, y, z
	else:
		print("IMU not initialized.")
		return None

mag_min = [float('inf')]*3
mag_max = [float('-inf')]*3	
def get_heading():
	x,y,z=get_mag()
	mag_values=[x,y,z]
	for i in range(3):
		mag_min[i] = min(mag_min[i],mag_values[i])
		mag_max[i] = max(mag_max[i],mag_values[i])
	mag_offset = [(mag_max[i]+mag_min[i])/2 for i in range(3)]
	mx_corr = x-mag_offset[0]
	my_corr = y-mag_offset[1]
	heading_rad = math.atan2(my_corr, mx_corr)
	heading_deg = math.degrees(heading_rad)
	if heading_deg < 0:
		heading_deg += 360
	print(heading_deg)
	return heading_deg



		


def read_hall_sensors():
	hall1 = GPIO.input(hall1_pin)
	hall2 = GPIO.input(hall2_pin)
	if hall1 == GPIO.LOW:
		print("Hall Sensor 1: Magnet detected")
	else:
		print("Hall Sensor 1: No magnet")
	if hall2 == GPIO.LOW:
		print("Hall Sensor 2: Magnet detected")
	else:
		print("Hall Sensor 2: No magnet")
	return hall1, hall2

if __name__ == "__main__":
	try:
		initialize_sensors()
		'''
		while not i2c.try_lock():
			pass
		print("runs")
		try:
			devices = i2c.scan()
			print("I2C addresses found:", [hex(address) for address in devices])
		finally:
			i2c.unlock()
		'''



		while True:			
			get_pitch()
			if GPIO.input(buttonPin) == GPIO.HIGH:
				blink()
				get_distances()
				get_color()
				get_accel()
				get_gyro()
				get_mag()
				read_hall_sensors()
				time.sleep(0.3)
			time.sleep(0.1)
	except KeyboardInterrupt:
		GPIO.cleanup()
		print("GPIO cleaned up. Exiting.")






