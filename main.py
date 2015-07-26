import os
import time
import RPi.GPIO as GPIO
from temp import getTemperature

MAX_FREQUENCY = 7.0
MIN_FREQUENCY = 3.0
#distance in cm
MAX_DISTANCE = 30.0

DIST_UPDATE_PERIOD = 1.0

TEMP_THRESHOLD = 20

BUZZ = 22
TRIG = 23
ECHO = 24

isBuzzing = False

def setup():
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)
  GPIO.setup(BUZZ,GPIO.OUT)
  GPIO.setup(TRIG,GPIO.OUT)
  GPIO.setup(ECHO,GPIO.IN)

def periodFromFrequency(frequency):
  return 1.0/frequency

def buzz(frequency):
  period = periodFromFrequency(frequency)
  GPIO.output(BUZZ, GPIO.HIGH)
  print("buzz")
  time.sleep(period/2.0)
  GPIO.output(BUZZ, GPIO.LOW)
  time.sleep(period/2.0)

def getDistance():
   
  #GPIO.output(TRIG, False)
  #time.sleep(2)
   
  GPIO.output(TRIG, True)
  time.sleep(0.00001)
  GPIO.output(TRIG, False)
  while GPIO.input(ECHO)==0:
    pulse_start = time.time()
  while GPIO.input(ECHO)==1:
    pulse_end = time.time()
  pulse_duration = pulse_end - pulse_start
  distance = pulse_duration * 17150
  distance = round(distance, 2)
  return distance

#distance in cm
def getFrequencyFromDistance(distance):
  if distance > MAX_DISTANCE:
    return 1
  return MIN_FREQUENCY + (MAX_FREQUENCY-MIN_FREQUENCY)*(1 - distance/MAX_DISTANCE)

#in miliseconds
frequency = 1
setup()

count = 1
lastFrequency = 1
buzzedLastTime = False

while(True):
  try:
    temp = getTemperature()
    print("Temp", temp)
    distance = getDistance()
    print("Dist", distance)
    frequency = getFrequencyFromDistance(distance)
    print("Freq", frequency)
    isBuzzing = (frequency > 1) and (temp > TEMP_THRESHOLD)
    if isBuzzing or buzzedLastTime:
      buzz(frequency if isBuzzing else lastFrequency)
      buzzedLastTime = isBuzzing
    print(count)
    count+=1
    lastFrequency = frequency
  except Exception as e:
    print(e)
    GPIO.cleanup()
    break

  
