import unittest
from ..discrete import Environment

class TestDiscreteEventSim(unittest.TestCase):

  def test_proper_ordering(self):
    """ Tests that events are executed in the proper order """
    e = Environment()
    
    first_var = False
    second_var = False

    def first_func():
      nonlocal first_var
      first_var = True

    def second_func():
      nonlocal second_var
      second_var = True

    e.add_event(first_func, 2)
    e.add_event(second_func, 12)

    e.do_next_event()

    self.assertTrue(first_var)
    self.assertFalse(second_var)

    e.do_next_event()

    self.assertTrue(first_var)
    self.assertTrue(second_var)     

  def test_run_methods(self):
    """ Tests that run_till_time and run function as expected """
    e = Environment()
    x = 0

    def func():
      nonlocal x
      x += 1

    for t in range(1, 123):
      e.add_event(func, t)

    e.run_till_time(37)

    self.assertEqual(x, 37)

    e.run()

    self.assertEqual(x, 122)



if __name__ == '__main__':
    unittest.main()