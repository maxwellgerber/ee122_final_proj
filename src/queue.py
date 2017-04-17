class Queue(object):
  """Queue discrete time simulator"""
  def __init__(self, env):
    self.env = env
    self.packets = []
    self.in_use = False
    self.curr_pkt = None
    self.all_pkts = []
    self.pkt_count = []

  def enqueue_packet(self):
    # Packet format: (service time, queueing start time, queueing stop time)
    service_time = self.service_rate
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
      t += self.arrival_rate
      self.env.add_event(self.enqueue_packet, t, "Packet Arrival")

    for i in range(1, int(t*20)):
      self.env.add_event(self.log_stats, i/20, "Logging statistics")

  def log_stats(self):
    i = len(self.packets) + self.in_use
    try:
      self.pkt_count[i] += 1
    except IndexError:
      self.pkt_count.append(0)
      self.log_stats()

  def print_distribution(self):
    total_dist = sum(self.pkt_count)
    print("Distribution of packets in system")
    print("#Pkts\tAcutal\tExpected\tError")
    for i, count in enumerate(self.pkt_count):
      actual_dist = count
      expected_dist = int(self.expected_dist(i) * total_dist)
      try:
        err = (actual_dist - expected_dist)/expected_dist * 100
      except ZeroDivisionError:
        err = 0
      print("{}:\t\t{}\t\t{}\t\t\t{:.2f}%".format(i, actual_dist, expected_dist, err))


  def expected_dist(self, i):
    return 0

  @property
  def arrival_rate(self):
    return 0

  @property
  def service_rate(self):
    return 0




