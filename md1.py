from src.discrete import Environment
from src.queue import Queue
from random import expovariate, seed
from tabulate import tabulate
from math import e
class MD1Queue(Queue):
  """MD1 Queue discrete time simulator"""
  def __init__(self, lamb, mu, env):
    super().__init__(env)
    self.lamb = lamb
    self.mu = mu

  @property
  def arrival_rate(self):
    return expovariate(self.lamb)

  @property
  def service_rate(self):
    return 1/self.mu

  def expected_dist(self, i):
    if i == 0:
      return 1 - 1/self.lamb
    l = 1/self.lamb
    return (1 - l) * (e**(i*l) - 1)


if __name__ == "__main__":
  seed(122)
  lamb = 130
  mu = 200
  N = int(1e5)

  QueueSim = Environment(verbosity=True)
  Q = MD1Queue(lamb, mu, QueueSim)
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
  expected_wait = rho/(2*mu*(1-rho))
  expected_overall = 1/mu + rho/(2*mu*(1-rho))
  expected_in_sys = rho + .5 * rho**2 / (1 - rho)
  tbl = [["Average wait time:", avg_wait],
         ["Average service time:", avg_wait],
         ["Overall time:", avg_service + avg_wait],
         ["Predicted wait time:", expected_wait],
         ["Wait time error:", 0],
         ["Predicted overall time:", expected_overall],
         ["Overall time error:", (avg_service + avg_wait - expected_overall) / expected_overall]]
  print(tabulate(tbl, floatfmt=".3f", tablefmt="fancy_grid"))
  Q.print_distribution()
  print("Num expected in sys = {}".format(expected_in_sys))


