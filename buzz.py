import os
import time
import RPi.GPIO as GPIO

MAX_FREQUENCY = 6.0
MIN_FREQUENCY = 2.0
#distance in cm
MAX_DISTANCE = 30.0

DIST_UPDATE_PERIOD = 1.0

BUZZ = 22
TRIG = 23
ECHO = 24

isBuzzing = False

def pinSetup():
  print("setup")
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
  print("Distance:",distance,"cm")
  return distance

#distance in cm
def getFrequencyFromDistance(distance):
  if distance > MAX_DISTANCE:
    return 0
  return MIN_FREQUENCY + (MAX_FREQUENCY-MIN_FREQUENCY)*(1 - distance/MAX_DISTANCE)


#in seconds
frequency = 1
pinSetup()

while(True):
  try:
    distance = getDistance()
    frequency = getFrequencyFromDistance(distance)
    print(frequency)
    isBuzzing = (frequency > 1)
    if isBuzzing:
      buzz(frequency)
  except:
    GPIO.cleanup()
