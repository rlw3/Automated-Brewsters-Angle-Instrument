from time import sleep
import RPi.GPIO as GPIO


STEP_PIN = 17
DIR_PIN = 18

CW = 1
CCW = 0
SPR = 800

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_PIN, GPIO.OUT)
GPIO.setup(STEP_PIN, GPIO.OUT)
GPIO.output(DIR_PIN, CW)

MODE = (5, 6, 13)
GPIO.setup(MODE, GPIO.OUT)
RESOLUTION = {'Full': (0,0,0),
              'Half': (1,0,0),
              '1/4': (0,1,0)}
GPIO.output(MODE, RESOLUTION['1/4'])

step_count = SPR
delay = 0.0208
for x in range(step_count):
    GPIO.output(STEP_PIN, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP_PIN, GPIO.LOW)
    sleep(delay)

sleep(.5)

GPIO.output(DIR_PIN, CCW)
for x in range (step_count):
    GPIO.output(STEP_PIN, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP_PIN, GPIO.LOW)
    sleep(delay)
