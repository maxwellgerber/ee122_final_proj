def quadratic(a, b, c):
  d = (b**2) - (4*a*c)
  sol1 = (-b-sqrt(d))/(2*a)
  sol2 = (-b+sqrt(d))/(2*a)
  return sol1, sol2