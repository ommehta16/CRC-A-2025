# just make a lil api to have motors go for a bit

import RPi.GPIO as GPIO
import time
from time import sleep
import multiprocessing as mp
import multiprocessing.connection as connection

TIME_INCREMENT:float = 0.5
MAX_PULL_WAIT:float = 5

def test():
    '''
    dance
    '''
    turn("left")
    sleep(0.5)
    stop()
    for i in range(3):
        turn("right") 
        sleep(1)
        stop()
        turn("left")
        sleep(1)
        stop()
    
    turn("right")
    sleep(0.5)
    stop()
    drive('forward')
    sleep(1)
    stop()
    drive('backward')
    sleep(1)
    stop()


def run(conn: connection.Connection):
    '''
    conn is a mp connection: we only need to pull data from it (it's like queue of data -- assume that it comes from a magical void)
    '''    
    lastPull = time.time()
    
    command = "sit"

    while True: # main loop
        now = time.time()

        while conn.poll() and (time.time()-now < TIME_INCREMENT or now-lastPull >= MAX_PULL_WAIT):
            lastPull = time.time()
            newData = conn.recv()

            if type(newData) is str: # command, time
                command = newData
            if type(newData) is tuple[int, float]:
                '''
                We'll need this later, but maybe start now?

                newData[0] == 0 --> stop
                newData[0] == 1 --> go forwards newData[1] cm
                newData[0] == 2 --> turn until facing at heading newData[0] degrees
                
                '''
                ...
        '''
        Do what command says to do here
        '''

        sleep(max(0,now+TIME_INCREMENT-time.time())) # just wait a bit so we dont go too fast

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
pwmA.ChangeDutyCycle(0)
pwmB.ChangeDutyCycle(0) 
pwmA.start(40)
pwmB.start(40)
driveSpeed = 40
turnSpeed = 40

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
    if direction == 'right':
        GPIO.output(motorA1, GPIO.LOW)
        GPIO.output(motorA2, GPIO.HIGH)
        GPIO.output(motorB1, GPIO.HIGH)
        GPIO.output(motorB2, GPIO.LOW)
    elif direction == 'left':
        GPIO.output(motorA1, GPIO.HIGH)
        GPIO.output(motorA2, GPIO.LOW)
        GPIO.output(motorB1, GPIO.LOW)
        GPIO.output(motorB2, GPIO.HIGH)
    pwmA.ChangeDutyCycle(turnSpeed)
    pwmB.ChangeDutyCycle(turnSpeed)


drive('forward')
sleep(5)
stop()
sleep(1)
drive('backward')
sleep(5)
turn('right')
sleep(5)
turn('left')
sleep(5)
