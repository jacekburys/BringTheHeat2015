import os
import time
import thread
import RPi.GPIO as GPIO
from temp import getTemperature

# 0 - temp & dist , 1 - dist only
MODE = 0
# ranges in cm
RANGES = [30.0, 100.0, 400.0]
modeRange = [0, 0]
MODE_SLEEP_TIME = 1


MAX_FREQUENCY = 7.0
MIN_FREQUENCY = 3.0
#distance in cm
MAX_DISTANCE = RANGES[0]
TEMP_THRESHOLD = 25

DIST_UPDATE_PERIOD = 1.0

#PINS
BUZZ = 22
TRIG = 23
ECHO = 24
BUTTON0 = 17
BUTTON1 = 18

isBuzzing = False

def setup():
  GPIO.setmode(GPIO.BCM)
  GPIO.setwarnings(False)
  GPIO.setup(BUZZ,GPIO.OUT)
  GPIO.setup(TRIG,GPIO.OUT)
  GPIO.setup(ECHO,GPIO.IN)
  GPIO.setup(BUTTON0,GPIO.IN)
  GPIO.setup(BUTTON1,GPIO.IN)

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
  global MODE
  buzzerMODE = MODE
  while True:
    if MODE != buzzerMode:
      buzzerMode = MODE
      processModeChange(buzzerMode)
    localFreq = frequency
    if (frequency > 1) and (temperature > TEMP_THRESHOLD):
      localFreq = frequency
      print "Buzz", localFreq
      buzz(localFreq)
      buzzSleep(localFreq)

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
      #count+=1
    except Exception as e:
      print(e)
      GPIO.cleanup()
      break

###

### MODE
# 0 - temp & dist , 1 - dist only
#MODE = 0
# ranges in cm
#RANGES = [30.0, 100.0, 400.0]
#modeRange = [0, 0]

def isButtonPressed(button):
  if button != BUTTON0 and button != BUTTON1:
    return False
  return GPIO.input(button)

# return True if mode changed, False otherwise
def updateMode():
  global MODE
  global modeRanges
  if isButtonPressed(BUTTON0):
    if MODE == 0:
      modeRanges[0] = (modeRanges[0]+1) % 3
    MODE = 0
    return True
  if isButtonPressed(BUTTON1):
    if MODE == 1:
      modeRanges[1] = (modeRanges[1]+1) % 3
    MODE = 1
    return True
  return False

def getMaxDistance():
  return RANGES[modeRanges[MODE]]

def buttonThreadCycle():
  global MAX_DISTANCE
  while True:
    changed = updateMode()
    if changed:
      print("Changed to mode", MODE)
      MAX_DISTANCE = RANGES[modeRanges[MODE]]
      time.sleep(MODE_SLEEP_TIME)

      
def processModeChange(mode):
  if mode == 0:
    GPIO.output(BUZZ, GPIO.HIGH)
    time.sleep(1.0)
    GPIO.output(BUZZ, GPIO.LOW)
    time.sleep(0.5)
  elif mode == 1:
    for _ in range(2):
      GPIO.output(BUZZ, GPIO.HIGH)
      time.sleep(1.0)
      GPIO.output(BUZZ, GPIO.LOW)
      time.sleep(0.5)

    
###

#in miliseconds
setup()

try:
  thread.start_new_thread(mainThreadCycle, ())
  thread.start_new_thread(buzzThreadCycle, ())
  thread.start_new_thread(buttonThreadCycle, ())
except:
  print("Error: unable to start the threads")

while 1:
  try:
    pass
  except:
    GPIO.output(BUZZ, GPIO.LOW)
    GPIO.cleanup()

