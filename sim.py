from src.discrete import Environment
from src.components import Car, StreetGraph, EuclideanNode

if __name__ == "__main__":
	g = StreetGraph(nodeCls = EuclideanNode)
	g.add_node(0, 0, 'A')
	g.add_node(10, 1, 'B')
	g.add_node(12, 12, 'C')
	g.add_edge('A', 'B')
	g.add_edge('B', 'C')
	print(g.shortest_path('A', 'C'))
	ferrari = g.add_car('A', 'C', 'One fast car', 3)

	MySimulation = Environment()

	def run_till_done():
	  print("The car is at x: {} y: {}".format(*ferrari.position()))
	  try:
	    ferrari.drive()
	    MySimulation.add_event(run_till_done, 1, "Driving the Car")
	  except:
	    print("All done driving.")


	MySimulation.add_event(run_till_done, 1, "Driving the Car")

	MySimulation.run()