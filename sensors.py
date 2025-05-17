import RPi.GPIO as GPIO
import time



import adafruit_vl53l0x
import adafruit_tcs34725
import board
import adafruit_lsm9ds0


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
		return r, g, b
	else:
		print("Color sensor not initialized.")
		return None

def get_imu_data():
	if imu:
		accel = imu.acceleration
		gyro = imu.gyro
		mag = imu.magnetic
		print(f"Accel: {accel}")
		print(f"Gyro: {gyro}")
		print(f"Mag: {mag}")
		return accel, gyro, mag
	else:
		print("IMU not initialized.")
		return None

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
		while not i2c.try_lock():
			pass
		print("runs")
		try:
			devices = i2c.scan()
			print("I2C addresses found:", [hex(address) for address in devices])
		finally:
			i2c.unlock()



		while True:
			if GPIO.input(buttonPin) == GPIO.HIGH:
				toggleLED()
				get_distances()
				get_color()
				get_imu_data()
				read_hall_sensors()
				time.sleep(0.3)
			time.sleep(0.05)
	except KeyboardInterrupt:
		GPIO.cleanup()
		print("GPIO cleaned up. Exiting.")






