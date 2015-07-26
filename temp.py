import sys
import numpy as np
import cv2
from pylepton import Lepton

TEMP_SIDE = 10

#THIS IS ACCURATE ONLY FOR 20 - 120 degrees
#for < 7700 return COLD
#for > 12800 return HOT
COEFFS = [-4.20829693e-11,-5.91950085e-07,4.79324337e-02,-3.01234009e+02]
f = np.poly1d(COEFFS)

#def bestSquare(lis, r):
#  x = len(lis)
#  if x == 0:
#    return 0
#  y = len(lis[0])
#  if r > min(x, y):
#    return 0
#  res = -10**9 
#  r2 = r*r
#  s = 0.0
#  for i in range(r):
#    for j in range(r):
#      s += lis[i][j][0]
#  res = s/r2
#  i = 0
#  j = 0
#  goingRight = True
#  while j+r <= y:
#    dx =  (1 if goingRight else -1)
#    if i+dx+r > x or i+dx<0:
#      if j+r >= y:
#        j+=1
#        break
#      goingRight = not goingRight
#      for k in range(r):
#        s -= lis[i+k][j][0]
#        s += lis[i+k][j+r][0]
#      j += 1
#      res = max(res, s/(r*r))
#      continue
#    else:
#      if goingRight:
#        for k in range(r):
#          s -= lis[i][j+k][0]
#          s += lis[i+r][j+k][0]
#        i+=1
#      else:
#        i-=1
#        for k in range(r):
#          s -= lis[i+r][j+k][0]
#          s += lis[i][j+k][0]
#      res = max(res, s/r2)
#  return res

def bestSquare(lis, side):
  w = len(lis)
  h = len(lis[0])
  m = -10**9
  mx = 0
  my = 0
  for x in range(w):
    for y in range(h):
      if lis[x][y][0] > m:
        m = lis[x][y][0]
        mx = x
        my = y
  r = side/2.0
  sum = 0.0
  count = 0
  for x in range(int(max(0,mx-r)), int(min(w,mx+r+1))):
    for y in range(int(max(0,my-r)), int(min(h,my+r+1))):
      sum += lis[x][y][0]
      count += 1
  return sum/count
      

def getTemperature():
  device = "/dev/spidev0.0"
  #print "before call"
  with Lepton(device) as l:
    a,_ = l.capture()
  #print "after call"
  return f(bestSquare(a, TEMP_SIDE))
