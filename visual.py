from src.discrete import Environment
from src.components import Car, StreetGraph, EuclideanNode
import matplotlib.pyplot as plt
import math
import imageio 


"""Vehicle Simulations"""
#car1 = Car((0,0),(5,5),'car1',g,3)


def drawNodes(i, xlist, ylist, r):
  carx = xlist[i]
  cary = ylist[i]
  for j in range(len(xlist)):
    if i == j:
      continue
    deltaX = carx - xlist[j]
    deltaY = cary - ylist[j]
    dist = math.sqrt(deltaX**2 + deltaY**2)
    if dist <= r:
      plt.plot([carx, xlist[j]], [cary, ylist[j]] ,'r')
      xavg = (carx + xlist[j])/2
      yavg = (cary + ylist[j])/2
      plt.text(xavg,yavg, r'' + str(round(dist,2)))
    else:
      pass
  return

#plt.plot(x, y, 'bo')

#ALL THIS NEEDS TO BE IN EVERY PLOT
#GRAPHSIZE = 10
#ticks = range(0, GRAPHSIZE + 1)
#x = [1,6,8,1,0,3,6,3,5]
#y = [1,3,5,6,2,7,0,3,1]
#plt.hold(True)

#plt.grid(b = True)
#plt.xticks(ticks)
#plt.yticks(ticks)
#plt.xlim(0, GRAPHSIZE)
#plt.ylim(0, GRAPHSIZE)
#drawNodes(4, x, y, 6)


#Testing Car Unit 
g = StreetGraph()
g.add_node(3, 0, 'A')
g.add_node(2, 12, 'B')
g.add_edge('A', 'B', 10)
ferrari = g.add_car('A', 'B', 'One fast car', 0.5)
f2 = g.add_car('A', 'B', 'blah2', 1)

numIter = 6 #number of driving iterations

images = []

for i in range(numIter):
  plt.figure(i)
  GRAPHSIZE = 15
  ticks = range(0, GRAPHSIZE + 1)
  plt.hold(True)
  plt.grid(b = True)
  plt.xticks(ticks)
  plt.yticks(ticks)
  plt.xlim(0, GRAPHSIZE)
  plt.ylim(0, GRAPHSIZE)

  xlist = []
  ylist = []

  for c in g._cars:
      x, y = c.position()
      xlist.append(x)
      ylist.append(y)
      plt.plot(x, y, 'bo')
      drawNodes(0, xlist,ylist, 3)
      c.drive()

  filename = 'fig' + str(i) + '.png'
  plt.savefig(filename)
  images.append(imageio.imread(filename))

exportname = "movie.gif"
kargs = { 'duration': 2 }
imageio.mimsave(exportname, images, 'GIF', **kargs)


 









