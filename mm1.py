from src.discrete import Environment
from src.queue import Queue
from random import expovariate, seed
from tabulate import tabulate

class MM1Queue(Queue):
  """MM1 Queue discrete time simulator"""
  def __init__(self, lamb, mu, env):
    super().__init__(env)
    self.lamb = lamb
    self.mu = mu

  @property
  def arrival_rate(self):
    return expovariate(self.lamb)

  @property
  def service_rate(self):
    return expovariate(self.mu)

  def expected_dist(self, i):
    rho = self.lamb/self.mu
    return (1-rho)*(rho**i)

if __name__ == "__main__":
  seed(122*122)
  lamb = 130
  mu = 200
  N = int(1e5)

  QueueSim = Environment(verbosity=False)
  Q = MM1Queue(lamb, mu, QueueSim)
  Q.generate_arrival_events(N)
  QueueSim.run()

  avg_wait = 0
  avg_service = 0
  for pkt in Q.all_pkts:
    avg_wait += pkt[2] - pkt[1] 
    avg_service += pkt[0]

  avg_wait = avg_wait/N
  avg_service = avg_service/N
  expected_wait = 1/(mu - lamb) - 1/mu
  expected_overall = 1/(mu - lamb)

  expected_in_sys = 1/(mu/lamb - 1)
  tbl = [["Average service time:", avg_service],
         ["Average wait time:", avg_wait],
         ["Predicted wait time:", expected_wait],
         ["Wait time error:", (avg_wait - expected_wait)/expected_wait],
         ["Overall time:", avg_service + avg_wait],
         ["Predicted overall time:", expected_overall],
         ["Overall time error:", (avg_service + avg_wait - expected_overall) / expected_overall]]
  print(tabulate(tbl, floatfmt=".6f", tablefmt="fancy_grid"))
  Q.print_distribution()
  print("Num expected in sys = {}".format(expected_in_sys))


