'''
OK GUYS
COMMON FORMATTING FOR LOCATION INCOMING!!

we're going to store direction as a dict

position state is passed around by the main guy
'''

import RPi.GPIO as GPIO
import time
from time import sleep
import multiprocessing as mp
import multiprocessing.connection as connection
import asyncio
import numpy as np

#Pins for Motor Drivers
motorA1 = 18
motorA2 = 16
motorApwm = 22
motorB1 = 10
motorB2 = 8
motorBpwm = 12

OFFSETS = [
    [0,1],
    [1,0],
    [0,-1],
    [-1,0],
]

# so increase direction is go right => + is right

#setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(motorA1,GPIO.OUT)
GPIO.setup(motorA2, GPIO.OUT)
GPIO.setup(motorApwm, GPIO.OUT)
pwmA = GPIO.PWM(motorApwm, 25000)

GPIO.setup(motorB1,GPIO.OUT)
GPIO.setup(motorB2, GPIO.OUT)
GPIO.setup(motorBpwm, GPIO.OUT)
pwmB = GPIO.PWM(motorBpwm, 25000)

pwmA.ChangeDutyCycle(0)
pwmB.ChangeDutyCycle(0) 
pwmA.start(40)
pwmB.start(40)
driveSpeed:float = 40
turn_speed:float = 40

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
    pwmA.ChangeDutyCycle(driveSpeed)
    pwmB.ChangeDutyCycle(driveSpeed)
    

def changeDriveSpeed(speed):
    driveSpeed = speed
    pwmA.ChangeDutyCycle(driveSpeed)
    pwmB.ChangeDutyCycle(driveSpeed)

class movement:
    @staticmethod
    async def turn(dir:int) -> None:
        '''
        Turn in the direction specified by `dir`
        A positive direction is right, negative is left, and 0 is stop
        '''

        if dir > 0:
            GPIO.output(motorA1, GPIO.LOW)
            GPIO.output(motorA2, GPIO.HIGH)
            GPIO.output(motorB1, GPIO.HIGH)
            GPIO.output(motorB2, GPIO.LOW)
        elif dir < 0:
            GPIO.output(motorA1, GPIO.HIGH)
            GPIO.output(motorA2, GPIO.LOW)
            GPIO.output(motorB1, GPIO.LOW)
            GPIO.output(motorB2, GPIO.HIGH)
        else:
            await movement.stop()
    
    @staticmethod
    async def drive(dir:int) -> None:
        '''
        
        '''
        if (dir=='forward'):
            GPIO.output(motorA1, GPIO.HIGH)
            GPIO.output(motorA2, GPIO.LOW)
            GPIO.output(motorB1, GPIO.HIGH)
            GPIO.output(motorB2, GPIO.LOW)

        elif (dir=='backward'):
            GPIO.output(motorA1, GPIO.LOW)
            GPIO.output(motorA2, GPIO.HIGH)
            GPIO.output(motorB1, GPIO.LOW)
            GPIO.output(motorB2, GPIO.HIGH)
        pwmA.ChangeDutyCycle(driveSpeed)
        pwmB.ChangeDutyCycle(driveSpeed)

    @staticmethod
    async def stop() -> None:
        '''
        Make it stop turning
        '''
        GPIO.output(motorA1, GPIO.LOW)
        GPIO.output(motorA2, GPIO.LOW)
        GPIO.output(motorB1, GPIO.LOW)
        GPIO.output(motorB2, GPIO.LOW)
        pwmA.ChangeDutyCycle(0)
        pwmB.ChangeDutyCycle(0)

    @staticmethod
    async def change_turn_speed(to:float) -> None:
        global turn_speed
        turn_speed = to

    @staticmethod
    async def change_drive_speed(to:float) -> None:
        global driveSpeed
        driveSpeed = to

    