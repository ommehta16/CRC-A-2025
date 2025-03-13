# just make a lil api to have motors go for a bit

import RPi.GPIO as GPIO
from time import sleep


#Pins for Motor Drivers
motorA1 = 29
motorA2 = 31
motorApwm = 33
motorB1 = 38
motorB2 = 40
motorBpwm = 35

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


def drive(direction,speed): #forward, backwards
    pwmA.ChangeDutyCycle(speed)
    pwmB.ChangeDutyCycle(speed) 
    if (direction=='forward'):
        GPIO.output(motorA1, GPIO.HIGH)
        GPIO.output(motorA2, GPIO.LOW)
        GPIO.output(motorB1, GPIO.HIGH)
        GPIO.output(motorB2, GPIO.LOW)

    elif (direction=='backward'):
        GPIO.output(motorA1, GPIO.LOW)
        GPIO.output(motorA2, GPIO.HIGH)
        GPIO.output(motorB1, GPIO.LOW)
        GPIO.output(motorB2, GPIO.HIGH)
    



