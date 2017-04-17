from src.discrete import Environment
from src.queue import Queue
from random import expovariate, seed

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
  seed(122)
  lamb = 20
  mu = 27
  N = 6000

  QueueSim = Environment(verbosity=True)
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
  print("Average wait time: \t\t\t{0:.4f}\nAverage service time: \t\t{1:.4f}\nOverall time: \t\t\t\t{2:.4f}".format(avg_wait, avg_service, avg_service + avg_wait))
  print("Predicted wait time: \t\t{0:.4f} \t\tSimulation error: {1:.2f}%".format(expected_wait, (avg_wait - expected_wait) / expected_wait * 100))
  print("Predicted overall time: \t{0:.4f} \t\tSimulation error: {1:.2f}%".format(expected_overall, (avg_service + avg_wait - expected_overall) / expected_overall * 100))
  Q.print_distribution()


