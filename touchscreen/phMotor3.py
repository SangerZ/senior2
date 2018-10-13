from time import sleep
import RPi.GPIO as GPIO
import time as t

volumeSpin = 1.2

def phSpin(vol):
    global volumeSpin
    DIR = 6
    STEP = 13

    CW = 1
    CCW = 0
    SPR = 200

    rounds = (vol*1000) / volumeSpin

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
    GPIO.output(DIR, CCW)
    
    delay = 0.0008

    for i in range(rounds):
        for j in range(SPR):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)
    GPIO.cleanup()
