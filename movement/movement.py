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
pwmA.ChangeDutyCycle(0)
pwmB.ChangeDutyCycle(0) 
pwmA.start(0)
pwmB.start(0)
driveSpeed = 0
turnSpeed = 0

def drive(direction): #forward, backwards
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
    

def changeDriveSpeed(speed):
    driveSpeed = speed
    pwmA.ChangeDutyCycle(driveSpeed)
    pwmB.ChangeDutyCycle(driveSpeed)

def changeTurnSpeed(speed):
    turnSpeed = speed


def stop():
    GPIO.output(motorA1, GPIO.LOW)
    GPIO.output(motorA2, GPIO.LOW)
    GPIO.output(motorB1, GPIO.LOW)
    GPIO.output(motorB2, GPIO.LOW)
    pwmA.ChangeDutyCycle(0)
    pwmB.ChangeDutyCycle(0)

def turn(direction):
    if direction == 'left':
        GPIO.output(motorA1, GPIO.LOW)
        GPIO.output(motorA2, GPIO.HIGH)
        GPIO.output(motorB1, GPIO.HIGH)
        GPIO.output(motorB2, GPIO.LOW)
    elif direction == 'right':
        GPIO.output(motorA1, GPIO.HIGH)
        GPIO.output(motorA2, GPIO.LOW)
        GPIO.output(motorB1, GPIO.LOW)
        GPIO.output(motorB2, GPIO.HIGH)
    pwmA.ChangeDutyCycle(turnSpeed)
    pwmB.ChangeDutyCycle(turnSpeed)

if __name__ == "__main__":
    drive("forward")
    sleep(0.1)
    stop()
    drive('backward')
    sleep(0.1)
    turn('right')
    sleep(0.1)
    turn('left')
