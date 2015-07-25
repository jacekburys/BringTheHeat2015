import sys
import numpy as np
import cv2
from pylepton import Lepton

#THIS IS ACCURATE ONLY FOR 20 - 120 degrees
#for < 7700 return COLD
#for > 12800 return HOT
COEFFS = [-4.20829693e-11,-5.91950085e-07,4.79324337e-02,-3.01234009e+02]
f = np.poly1d(COEFFS)

def getTemperature():
  device = "/dev/spidev0.0"
  with Lepton(device) as l:
    a,_ = l.capture()
  x = len(a)
  y = len(a[0])
  sum = 0.0
  count = 0.0
  for i in range(x//2 - 5, x//2 + 5):
    for j in range(y//2 - 5, y//2 + 5):
      count+=1
      sum+=a[i][j][0]
  res = sum/count
  return res
