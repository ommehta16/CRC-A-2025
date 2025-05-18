

import RPi.GPIO as GPIO
from time import sleep
#GPIO.setwarnings(False)

# NOT USING THIS ONE
#Pins for Motor Drivers
motorA1 = 18
motorA2 = 16
motorApwm = 22
motorB1 = 10
motorB2 = 8
motorBpwm = 12

#setup

GPIO.setmode(GPIO.BOARD)
GPIO.setup(motorA1,GPIO.OUT)
GPIO.setup(motorA2, GPIO.OUT)
GPIO.setup(motorApwm, GPIO.OUT)
GPIO.setup(motorB1,GPIO.OUT)
GPIO.setup(motorB2, GPIO.OUT)
GPIO.setup(motorBpwm, GPIO.OUT)
pwmA = GPIO.PWM(motorApwm, 25000)
pwmB = GPIO.PWM(motorBpwm, 25000)
pwmA.start(0)
pwmB.start(0)

GPIO.output(motorA1, GPIO.HIGH)
GPIO.output(motorA2, GPIO.LOW)
GPIO.output(motorB1, GPIO.HIGH)
GPIO.output(motorB2, GPIO.LOW)
pwmA.ChangeDutyCycle(100)
pwmB.ChangeDutyCycle(100)
sleep(5)
GPIO.output(motorA1, GPIO.LOW)
GPIO.output(motorA2, GPIO.HIGH)
GPIO.output(motorB1, GPIO.LOW)
GPIO.output(motorB2, GPIO.HIGH)
sleep(5)
pwmA.stop()
pwmB.stop()
GPIO.cleanup()

