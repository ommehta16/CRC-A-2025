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
    async def drive(dir:int=1) -> None:
        '''
        
        '''
        if (dir==1):
            GPIO.output(motorA1, GPIO.HIGH)
            GPIO.output(motorA2, GPIO.LOW)
            GPIO.output(motorB1, GPIO.HIGH)
            GPIO.output(motorB2, GPIO.LOW)

        elif (dir== -1):
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

    @staticmethod
    async def move_tiles(n:int=1) -> int:
        '''BRANDEN PLS IMPLEMENT THIS!!!'''
        raise NotImplementedError()
        # moves n tiles forwards, then *reports the vertical change*
        return 0

    @staticmethod
    async def rotate(by:int) -> None:
        '''BRANDEN PLS IMPLEMENT THIS AS WELL'''
        
        # just turn the bot by `by` 90 degree rotations (+3 --> 3 turns right, -3 --> 3 turns left)
        #

def test():
    print("forwards")
    asyncio.run(movement.drive(1))
    time.sleep(1)
    print("rigth")
    asyncio.run(movement.turn(1))
    time.sleep(0.1)
    print("left")
    asyncio.run(movement.turn(-1))
    time.sleep(0.1)
    print("stop")
    asyncio.run(movement.turn(0))
    time.sleep(0.1)
    print("stop but again")
    asyncio.run(movement.stop())
    time.sleep(0.1)
    print("slow down")
    asyncio.run(movement.change_drive_speed(20))
    print("forwards")
    asyncio.run(movement.drive(1))
    time.sleep(0.1)
    print("stop")
    asyncio.run(movement.stop())

    print("forwards")
    asyncio.create_task(movement.drive(1))
    time.sleep(1)
    print("stop")
    asyncio.run(movement.stop())

if __name__ == "__main__":
    print("dfsjakhfjkdsahk")
    test()
    print("dafjdshk odne")