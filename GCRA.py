from discrete import Environment

class LeakyBucket(object):
  """Leaky Bucket GCRA example from Feb 22 Discussion"""
  def __init__(self, T, tau):
    self.T = T
    self.X_max = T + tau
    self.X = 0
    self.carts_filled = 0
    
  def set_X(self, val):
    self.X = val
    
  def add_drop(self, dropsize):
    self.X = min(self.X_max, self.X + dropsize)
    
  def handle_cart_arrival(self):
    if self.X >= self.T:
      print("Added {} worth of stuff to a cart".format(self.T))
      self.X -= self.T
      self.carts_filled += 1
      return True
    else:
      print("Could not fill cart at this time")
      return False


if __name__ == "__main__":
  BucketSim = Environment()
  B = LeakyBucket(10, 3)
  B.set_X(13)

  # Add all droplets
  for i in range(1,29):
    BucketSim.add_event(lambda: B.add_drop(1), i-.1, "Droplet")

  # Add all scheduled cart arrivals
  for i in [1, 6, 12, 19, 28]:
    BucketSim.add_event(B.handle_cart_arrival, i, "Cart")
    
  print("Starting Leaky Bucket simulation")
  BucketSim.run()
  print("Done - Successfully filled {} carts in {} units of time".format(B.carts_filled, BucketSim.time_elapsed))
