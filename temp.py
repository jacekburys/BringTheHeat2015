import numpy as np

#THIS IS ACCURATE ONLY FOR 20 - 120 degrees
#for < 7700 return COLD
#for > 12800 return HOT
COEFFS = [-4.20829693e-11,-5.91950085e-07,4.79324337e-02,-3.01234009e+02]

f = np.poly1d(COEFFS)
while(True):
  try:
    t = int(input())
    print(f(t))
  except:
    break
