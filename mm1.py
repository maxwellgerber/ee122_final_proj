from src.discrete import Environment
from random import expovariate, seed

class MM1Queue(object):
  """Leaky Bucket GCRA example from Feb 22 Discussion"""
  def __init__(self, lamb, mu, env):
    self.lamb = lamb
    self.mu = mu
    self.env = env
    self.packets = []
    self.in_use = False
    self.curr_pkt = None
    self.all_pkts = []

  def enqueue_packet(self):
    # Packet format: (service time, queueing start time, queueing stop time) 
    service_time = expovariate(self.mu)
    pkt = (service_time, self.env.time_elapsed, None)
    self.packets.append(pkt)
    self.service_packet()

  def service_packet(self):
    if not self.in_use and len(self.packets):
      pkt = self.packets.pop(0)
      self.curr_pkt = pkt[0], pkt[1], self.env.time_elapsed
      service_time = pkt[0]
      self.env.add_event(self.finish_serving_packet, service_time, "Packet Departure")
      self.in_use = True

  def finish_serving_packet(self):
    self.all_pkts.append(self.curr_pkt)
    self.curr_pkt = None
    self.in_use = False
    self.service_packet()

  def generate_arrival_events(self, N):
    t = 0
    for _ in range(N):
      t += expovariate(self.lamb)
      self.env.add_event(self.enqueue_packet, t, "Packet Arrival")

if __name__ == "__main__":
  seed(122)
  lamb = 20
  mu = 27
  N = 5000

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



