import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def getData():
  res = []
  for line in open("data.txt", "r"):
    temp, val = list(map(int, line.split()))
    res.insert(0,(val,temp))
  print(res)
  return res

points = np.array(getData())
x = points[:,0]
y = points[:,1]

z = np.polyfit(x, y, 3)
print(z)
f = np.poly1d(z)

print("ok")

newX = np.linspace(x[0],x[-1],50)
newY = f(newX)

plt.plot(x,y,'o',newX,newY)
plt.xlim(x[0]-1, x[-1]+1)
plt.show()
