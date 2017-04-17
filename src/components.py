import copy
import math

from util import quadratic

class Car(object):
  """web enabled car"""
  def __init__(self, source, destination, label, sg, speed, rad = 1):
    self._source = source
    self._destination = destination
    self._label = label
    # Parent street graph this car cruises on
    self._sg = sg
    self._speed = speed
    self._next_node_dist_traveled = 0
    self._linkLife = dict()
    self._rad = rad
    self._calculate_route()

  def getSpeed(self):
    return self._speed

  def getNextNode(self):
    return self._next_node

  def getRad(self):
    return self._rad

  def getLinkLife(self, target_car_label):
    if target_car_label in self._linkLife:
      return self._linkLife[target_car]
    else:
      return None

  def setLinkLife(self, target_car_label, linkVal):
    self._linkLife[target_car] = linkVal

  def resetLinks(self):
    self._linkLife.clear()

  def set_speed(self, speed):
    self._speed = speed

  def _calculate_route(self):
    route, _ = self._sg.shortest_path(self._source, self._destination)
    self._last_node = route.pop(0)
    self._route = route
    self._update_next_dest()

  def _update_next_dest(self):
    if self._route:
      self._next_node = self._route.pop(0)
      self._next_node_dist = self._sg.get_edge(self._last_node, self._next_node)
    else:
      self._next_node = None
      self._next_node_dist = 0
      self._next_node_dist_traveled = 0

  def drive(self):
    if self._next_node:
      self._next_node_dist_traveled += self._speed
      while True:
        if self._next_node and self._next_node_dist_traveled >= self._next_node_dist:
          self._next_node_dist_traveled -= self._next_node_dist
          print("Passing {}".format(self._next_node))
          self._last_node = self._next_node
          self._update_next_dest()
        else:
          break
    else:
      raise Exception("We are done driving")

  def position(self):
    # Calculates the position as a weighted average of the prev and next nodes
    if(self._next_node_dist == 0):
      # We are already there!
      return self._sg.get_xy_coords(self._destination)
      
    x0, y0 = self._sg.get_xy_coords(self._last_node)
    x1, y1 = self._sg.get_xy_coords(self._next_node)
    theta = math.atan2(y1-y0,x1-x0)
    x = x0 + self._next_node_dist_traveled * math.cos(theta)
    y = y0 + self._next_node_dist_traveled * math.sin(theta)
    return  x, y

#########################################################################################

class Node(object):
  """Simple node in a graph containing a label, x + y coordinates for drawing, and a neighbors map"""
  def __init__(self, x, y, label):
    self._x = x
    self._y = y
    self._label = label
    self._neighbors = {}
    
  def __repr__(self):
    return self._label

  def add_neighbor(self, other, dist = 1):
    assert isinstance(other, Node)
    assert other not in self._neighbors
    self._neighbors[other] = dist

  def neighbors(self):
    return self._neighbors.items()


class EuclideanNode(Node):
  """Node in a graph representing a single street intersection. Calculates Euclidian distance between other's x and y"""
  def __init__(self, *args):
    super(EuclideanNode, self).__init__(*args)

  def add_neighbor(self, other, dist = 1):
    assert isinstance(other, Node)
    assert other not in self._neighbors
    self._neighbors[other] = math.sqrt((self._x - other._x)**2 + (self._y - other._y)**2)


class ManhattanNode(Node):
  """Node in a graph representing a single street intersection. Calculates Manhattan distance between other's x and y"""
  def __init__(self, *args):
    super(ManhattanNode, self).__init__(*args)

  def add_neighbor(self, other, dist = 1):
    assert isinstance(other, Node)
    assert other not in self._neighbors
    self._neighbors[other] = abs(self._x - other._x) + abs(self._y - other._y)


class StreetGraph(object):
  """Graph class containing information and methods related to roadways"""
  def __init__(self, nodeCls = Node, carCls = Car):
    self._nodes = set()
    self._cars = set()
    self._nodeCls = nodeCls
    self._carCls = carCls

  def add_car(self, origin, destination, label, speed = 1):
    delorian = self._carCls(origin, destination, label, self, speed)
    self._cars.add(delorian)
    return delorian

  def add_node(self, x, y, label):
    node = self._nodeCls(x, y, label)
    self._nodes.add(node)

  def add_edge(self, label1, label2, dist = 1):
    node1 = self._node_from_label(label1)
    node2 = self._node_from_label(label2)
    node1.add_neighbor(node2, dist)
    node2.add_neighbor(node1, dist)

  def get_edge(self, label1, label2):
    node1 = self._node_from_label(label1)
    node2 = self._node_from_label(label2)
    return node1._neighbors[node2]

  def get_xy_coords(self, label):
    node = self._node_from_label(label)
    return node._x, node._y 

  def _node_from_label(self, label):
    for n in self._nodes:
      if n._label == label:
        return n
    raise Exception("No node could be found corresponding to label: {}".format(label))

  def _car_from_label(self, label):
    for c in self._cars:
      if c._label == label:
        return c
    raise Exception("No car could be found corresponding to label: {}".format(label))

  def get_car_velocity(self, car):
    ''' Returns a tuple of (vel_x, vel_y) corresponding to the car matching LABEL in the street graph'''
    x, y = car.position()
    sp = car.getSpeed()
    dest_x, dest_y = self.get_xy_coords(car.getNextNode())
    vx1 = dest_x - x
    vy1 = dest_y - y
    vnorm1 = math.sqrt(vx^2 + vy^2)
    try:
      vel_x = vx / vnorm1 * sp
      vel_y = vy / vnorm1 * sp
      return vel_x, vel_y
    except ZeroDivisionError:
      return 0, 0

  def shortest_path(self, label1, label2):
    # Returns a list of labels corresponding to the shortest path from label1 to label2 and the total distance
    s = self._node_from_label(label1)
    t = self._node_from_label(label2)
    if not s or not t:
      return

    dist = {}
    prev = {}

    for n in self._nodes:
      dist[n] = math.inf
      prev[n] = None

    dist[s] = 0

    Q = copy.copy(self._nodes)
    while Q:
      # O(n^2) time because I'm a piece of human garbage
      _, smallest = min([ (dist[n], n) for n in Q ], key = lambda x: x[0])
      Q.remove(smallest)
      for neighbor, ndist in smallest.neighbors():
        newdist = dist[smallest] + ndist
        if newdist < dist[neighbor]:
          dist[neighbor] = newdist
          prev[neighbor] = smallest

    path = []
    bt = t
    while bt:
      path.insert(0, bt._label)
      bt = prev[bt]

    return path, dist[t]

#########################################################################################

class AccessPoint(object):
  """
  Simple node in a graph containing x + y coordinates for drawing
  Represents unlimited connection to the internet
  """
  def __init__(self, x, y):
    self._x = x
    self._y = y

  def position(self):
    return self._x, self._y


class RoutingGraph(Object):
  """Routing Graph keeps track of the LinkLife/Edges"""
  def __init__(self, sGraph):
    self._cars = sGraph._cars 
    self._edges = dict()

  def update_edges(self):
    for c in self._nodes:
      for k, v in c._linkLife:
        self._edges[c] = (k, v)

  def set_link_lifetimes(self):
    # Sets Link Life of car (edges)
    for c in sGraph._cars:
      c.resetLink()
      x, y = c.position()
      for ci in sGraph._cars:
        if (c == ci):
          continue
        xi, yi = ci.position()
        dX = x - xi
        dY = y - yi
        dist = math.sqrt(dX**2 + dY**2)
        if dist > c.getRad() or dist > ci.getRad():
          continue
        else:
          linkVal = detLinkLife(c, ci, sGraph)
          c.setLinkLife(ci, linkVal)

  @classmethod
  def determine_link_life(cls, car1, car2, sGraph):
    a_x, a_y = car1.position()
    b_x, b_y = car2.position()
    av_x, av_y = sGraph.get_car_velocity(car1.label)
    bv_x, bv_y = sGraph.get_car_velocity(car2.label)
    a = a_x - b_x
    b = a_y - b_y
    c = av_x - bv_x
    d = av_x - bv_y
    
    c_0 = a^2 + b^2 - car1.getRad()^2
    c_1 = 2*a*c + 2*b*d
    c_2 = c^2 + d^2
    
    try:
      return max(quadratic(c_2, c_1, c_0))
    except ZeroDivisionError:
      return inf







