from heapq import heappop, heappush

class NoEventError(Exception):
  pass

class Environment(object):
  """Parent environment used to run Discrete Event Simulations"""
  def __init__(self, verbosity = False):
    self.time_elapsed = 0
    self.event_queue = []
    self.v = verbosity
    self.regular_events = []
    self.event_count = 0
    
  def add_event(self, eventfunc, time, message="some"):
    # Events are just functions. When the function is executed, the event is done
    # Time is relative- an event with time=5 added at time_elapsed=2 will occur at time_elapsed=7
    execution_time = self.time_elapsed + time
    heappush(self.event_queue, (execution_time, eventfunc, message))
    
  def add_fixed_event(self, eventfunc, time, message="some"):
    # Adds an event at an absolute time - not relative
    self.add_event(eventfunc, time-self.time_elapsed, message)

  def add_regular_event(self, eventfunc, interval):
    # Adds an event that occurs every INTERVAL number of events- for logging purposes
    self.regular_events.append((interval, eventfunc))

  def do_regular_events(self):
    for interval, eventfunc in self.regular_events:
      if self.event_count % interval == 0:
        eventfunc()

  def do_next_event(self):
    # Pop the soonest event off the heap and run it
    # Decrease the time of all the other events
    try:
      time, eventfunc, message = heappop(self.event_queue)
      assert time > 0
      self.time_elapsed = time
      self.v and print("Executing {} event at time {}".format(message, self.time_elapsed))
      # self.event_queue = [(t-time, e, m) for t,e,m in self.event_queue]
      eventfunc()
      self.event_count += 1
      self.do_regular_events()
    except IndexError:
      self.v and print("No events left in queue")
      raise NoEventError()
      
  def run(self):
    # Run events until there are no more in the queue
    while True:
      try:
        self.do_next_event()
      except NoEventError:
        break

  def run_till_time(self, time):
    # Run till total time elapsed is greater than TIME
    while self.time_elapsed < time:
      self.do_next_event()
