import unittest
from ..components import StreetGraph, EuclideanNode, ManhattanNode

class TestGraph(unittest.TestCase):

  def test_dijstra(self):
    sg = StreetGraph()
    sg.add_node(0,0, "A")
    sg.add_node(0,1, "B")
    sg.add_node(1,1, "C")
    sg.add_node(1,0, "D")

    sg.add_edge("A", "B", 24)
    sg.add_edge("A", "D", 20)
    sg.add_edge("A", "C", 3)
    sg.add_edge("D", "C", 12)

    path, dist = sg.shortest_path("A", "D")
    self.assertEqual(dist, 15)
    self.assertEqual(path, ["A", "C", "D"])


class TestEuclideanNode(unittest.TestCase):

  def test_distance(self):
    sg = StreetGraph(nodeCls = EuclideanNode)
    sg.add_node(1, 1, "A")
    sg.add_node(2, 2, "B")
    sg.add_edge("A", "B")
    self.assertAlmostEqual(sg.get_edge("A", "B"), 2**.5)

class TestManhattanNode(unittest.TestCase):
  
  def test_distance(self):
    sg = StreetGraph(nodeCls = ManhattanNode)
    sg.add_node(2, 3, "A")
    sg.add_node(10, 5, "B")
    sg.add_edge("A", "B")
    self.assertEqual(sg.get_edge("A", "B"), 10)

if __name__ == '__main__':
    unittest.main()