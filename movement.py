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
import sensors

#Pins for Motor Drivers
motorA1 = 1
motorA2 = 7
motorApwm = 12
motorB1 = 24
motorB2 = 23
motorBpwm = 18

OFFSETS = [
    [0,1],
    [1,0],
    [0,-1],
    [-1,0],
]

# so increase direction is go right => + is right

#setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(motorA1,GPIO.OUT)
GPIO.setup(motorA2, GPIO.OUT)
GPIO.setup(motorApwm, GPIO.OUT)
pwmA = GPIO.PWM(motorApwm, 25000)

GPIO.setup(motorB1,GPIO.OUT)
GPIO.setup(motorB2, GPIO.OUT)
GPIO.setup(motorBpwm, GPIO.OUT)
pwmB = GPIO.PWM(motorBpwm, 25000)

GPIO.output(motorA1, GPIO.LOW)
GPIO.output(motorA2, GPIO.LOW)
GPIO.output(motorB1, GPIO.LOW)
GPIO.output(motorB2, GPIO.LOW)

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
    async def move_tiles(n:int=1) -> float: #TODO
        '''BRANDEN PLS IMPLEMENT THIS!!!'''
        raise NotImplementedError()
        # moves n tiles forwards, then *reports the vertical change* as a proportion of 25cm
        # This should literally just move the robot n tiles laterally forwards. It MUST adjust 
        # for inclines, and (should? idk if it has to ?) adjust for speed bumps to avoid us losing 
        # accuracy. 
        # 
        # (Accuracy losses build up because I *didn't add a recalbration for position in main*.)
        #  ^^ You can try to ask chat for this, but like 50/50 chance it blows up the rest of it so idk :shrug:
        return 0

    @staticmethod
    async def rotate(by:int) -> None: #TODO
        '''BRANDEN PLS IMPLEMENT THIS AS WELL'''
        raise NotImplementedError()
        # just turn the bot by `by` 90 degree rotations (+3 --> 3 turns right, -3 --> 3 turns left)
        # 
        # Turns 90 degrees right `by` times. If `by` is negative, it turns left |by| times. If by
        # is positive, it turns right |by| times. Preferrably, the `by` 90 degree turns would be one,
        # fluid action (i.e. to turn 180 degrees left, we go directly to 180 instead of pausing at 90).
        # 
        # Optionally, you can do some math to ensure that we never make unnecessarily big rotations
class output:
    @staticmethod
    async def blink():
        sensors.blink(6)
    @staticmethod
    def eject(): #TODO
        '''Eject 1 package from the mag'''
        raise NotImplementedError()
    
        '''
        
        '''


def test():
    print("forwards")
    asyncio.run(movement.drive(1))
    time.sleep(1)
    asyncio.run(movement.stop())
    
def test2():
    asyncio.run(movement.drive())
    while True:
        sensors.read_hall_sensors()
        time.sleep(0.1)
if __name__ == "__main__":
    print("dfsjakhfjkdsahk")
    test()
    #test2()
    print("dafjdshk odne")
    GPIO.cleanup()
