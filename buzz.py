import os
import time
import RPi.GPIO as GPIO

buzzPin = 22

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(buzzPin ,GPIO.OUT)

def period(frequency):
  return 1.0/frequency

#in miliseconds
frequency = 1
duration = 0.5

while(True):
  GPIO.output(buzzPin, GPIO.HIGH)
  sleep(duration)
  GPIO.output(buzzPin, GPIO.LOW)
  sleep(period(frequency))

  
