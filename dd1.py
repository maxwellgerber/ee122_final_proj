from src.discrete import Environment
from src.queue import Queue
from random import expovariate, seed
from tabulate import tabulate

class DD1Queue(Queue):
  """DD1 Queue discrete time simulator"""
  def __init__(self, lamb, mu, env):
    super().__init__(env)
    self.lamb = lamb
    self.mu = mu

  @property
  def arrival_rate(self):
    return 1/self.lamb

  @property
  def service_rate(self):
    return 1/self.mu

  def expected_dist(self, i):
    rho = self.lamb/self.mu
    return rho if i else 1 - rho


if __name__ == "__main__":
  seed(122)
  lamb = 130
  mu = 200
  N = 100000

  QueueSim = Environment(verbosity=True)
  Q = DD1Queue(lamb, mu, QueueSim)
  Q.generate_arrival_events(N)
  QueueSim.run()

  avg_wait = 0
  avg_service = 0
  for pkt in Q.all_pkts:
    avg_wait += pkt[2] - pkt[1]
    avg_service += pkt[0]

  avg_wait = avg_wait/N
  avg_service = avg_service/N

  rho = lamb/mu
  expected_wait = rho
  expected_overall = 1/mu

  tbl = [["Average wait time:", avg_wait],
         ["Average service time:", avg_wait],
         ["Overall time:", avg_service + avg_wait],
         ["Predicted wait time:", expected_wait],
         ["Wait time error:", 0],
         ["Predicted overall time:", expected_overall],
         ["Overall time error:", (avg_service + avg_wait - expected_overall) / expected_overall]]
  print(tabulate(tbl, floatfmt=".3f", tablefmt="fancy_grid"))
  Q.print_distribution()
