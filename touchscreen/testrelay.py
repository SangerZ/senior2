import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
ma = 17
mb = 27
mc = 22
GPIO.setup(ma, GPIO.OUT)
GPIO.setup(mb, GPIO.OUT)
GPIO.setup(mc, GPIO.OUT)
GPIO.output(ma, GPIO.HIGH)
GPIO.output(mb, GPIO.HIGH)
GPIO.output(mc, GPIO.HIGH)

GPIO.output(ma, GPIO.LOW)
time.sleep(20)
GPIO.output(ma, GPIO.HIGH)
time.sleep(10)
GPIO.output(mb, GPIO.LOW)
time.sleep(20)
GPIO.output(mb, GPIO.HIGH)

GPIO.cleanup()
