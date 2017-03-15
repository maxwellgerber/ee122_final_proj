import unittest
from ..components import StreetGraph, EuclideanNode

class TestStringMethods(unittest.TestCase):

  def assert_car_position(self, expected, actual):
    self.assertAlmostEqual(expected[0], actual[0])
    self.assertAlmostEqual(expected[1], actual[1])


  def test_car_speed(self):
    g = StreetGraph()
    g.add_node(0, 0, 'A')
    g.add_node(0, 10, 'B')
    g.add_edge('A', 'B', 10)
    ferrari = g.add_car('A', 'B', 'One fast car', 1)
    self.assert_car_position(ferrari.position(), (0,0))
    ferrari.drive()
    self.assert_car_position(ferrari.position(), (0,1))
    ferrari.set_speed(8)
    ferrari.drive()
    x, y = ferrari.position()
    self.assertAlmostEqual(x, 0)
    self.assertAlmostEqual(y, 9)

  def test_car_stops(self):
    g = StreetGraph()
    g.add_node(0, 0, 'A')
    g.add_node(0, 10, 'B')
    g.add_edge('A', 'B', 10)
    ferrari = g.add_car('A', 'B', 'One fast car', 12)
    self.assertEqual(ferrari.position(), (0, 0))
    ferrari.drive()
    self.assert_car_position(ferrari.position(), (0,10))

  def test_done_driving_exception(self):
    g = StreetGraph()
    g.add_node(0, 0, 'A')
    g.add_node(0, 10, 'B')
    g.add_edge('A', 'B', 10)
    ferrari = g.add_car('A', 'B', 'One fast car', 10)
    ferrari.drive()
    self.assertRaises(Exception, ferrari.drive)

  def test_car_turns(self):
    g = StreetGraph(nodeCls = EuclideanNode)
    g.add_node(0, 0, 'A')
    g.add_node(0, 10, 'B')
    g.add_node(10, 10, 'C')
    g.add_edge('A', 'B')
    g.add_edge('B', 'C')
    ferrari = g.add_car('A', 'C', 'One fast car', 3)
    ferrari.drive()
    ferrari.drive()
    ferrari.drive()
    self.assert_car_position(ferrari.position(), (0,9))
    ferrari.drive()
    self.assert_car_position(ferrari.position(), (2,10))

  def test_car_turns_multiple(self):
    """ ls

    B - C   F - G
    |   |   |   |
    A   D - E   H
    """
    g = StreetGraph(nodeCls = EuclideanNode)
    g.add_node(0, 0, 'A')
    g.add_node(0, 1, 'B')
    g.add_node(1, 1, 'C')
    g.add_node(1, 0, 'D')
    g.add_node(2, 0, 'E')
    g.add_node(2, 1, 'F')
    g.add_node(3, 1, 'G')
    g.add_node(3, 0, 'H')
    g.add_edge('A', 'B')
    g.add_edge('B', 'C')
    g.add_edge('C', 'D')
    g.add_edge('D', 'E')
    g.add_edge('E', 'F')
    g.add_edge('F', 'G')
    g.add_edge('G', 'H')
    ferrari = g.add_car('A', 'H', 'One fast car', .5)
    ferrari.drive()
    print("speed change whee")
    self.assert_car_position(ferrari.position(), (0,.5))
    ferrari.set_speed(6)
    ferrari.drive()
    self.assert_car_position(ferrari.position(), (3,.5))


if __name__ == '__main__':
    unittest.main()