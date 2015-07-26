
import os
import time
import threading
import RPi.GPIO as GPIO
BUZZ = 22
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(BUZZ,GPIO.OUT)
GPIO.output(BUZZ, GPIO.LOW)
