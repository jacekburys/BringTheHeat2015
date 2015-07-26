import os
import time
import thread
import RPi.GPIO as GPIO
from temp import getTemperature

MAX_FREQUENCY = 7.0
MIN_FREQUENCY = 3.0
#distance in cm
MAX_DISTANCE = 30.0
TEMP_THRESHOLD = 25

DIST_UPDATE_PERIOD = 1.0


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
  if frequency < MIN_FREQUENCY or frequency > MAX_FREQUENCY:
    return
  period = periodFromFrequency(frequency)
  GPIO.output(BUZZ, GPIO.HIGH)
  print("buzz")
  time.sleep(period/2.0)

def buzzSleep(frequency):
  if frequency < MIN_FREQUENCY or frequency > MAX_FREQUENCY:
    return
  period = periodFromFrequency(frequency)
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

### MULTITHREADING
frequency = 1
temperature = 20

def buzzThreadCycle():
  global frequency
  global temperature
  while True:
    localFreq = frequency
    if (frequency > 1) and (temperature > TEMP_THRESHOLD):
      localFreq = frequency
      print "Buzz", localFreq
      buzz(localFreq)
      buzzSleep(localFreq)
    print "BUZZ OK", temperature, localFreq

def mainThreadCycle():
  count = 1
  global frequency
  global temperature
  while True:
    try:
      temperature = getTemperature()
      #print("Temp", temperature)
      distance = getDistance()
      #print("Dist", distance)
      frequency = getFrequencyFromDistance(distance)
      #print("Freq", frequency)
      #print(count)
      count+=1
    except Exception as e:
      print(e)
      GPIO.cleanup()
      break

###

#in miliseconds
setup()


try:
  thread.start_new_thread(mainThreadCycle, ())
  thread.start_new_thread(buzzThreadCycle, ())
except:
  print("Error: unable to start the threads")

while 1:
  try:
    pass
  except:
    GPIO.output(BUZZ, GPIO.LOW)
    GPIO.cleanup()

