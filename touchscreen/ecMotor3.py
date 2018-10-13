from time import sleep
import RPi.GPIO as GPIO
import time as t

volumeSpin = 1.2

def ecSpin(vol):
    global volumeSpin
    DIR = 20
    STEP = 21
    DIR2 = 19
    STEP2 = 26

    CW = 1
    CCW = 0
    SPR = 200

    rounds = (vol*1000) / volumeSpin

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(DIR2, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
    GPIO.setup(STEP2, GPIO.OUT)
    GPIO.output(DIR, CCW)
    GPIO.output(DIR2, CCW)
    
    delay = 0.0008

    for i in range(rounds):
        for j in range(SPR):
            GPIO.output(STEP, GPIO.HIGH)
            GPIO.output(STEP2, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            GPIO.output(STEP2, GPIO.LOW)
            sleep(delay)
    GPIO.cleanup()
