"""
Problem developed by Jean-Noel Monette, Uppsala University

This model finds a shortest program to compute a linear combination of variables.
The difficulty is that the program can only use the binary plus and the unary minus.
To symbolic program is linked to a set of examples against which it must conform.
This is one part of a counter-example guided loop, where examples are added when a counter
example is found for the generated programs.
The counter-example generation is the other part and not included in this problem, which
only does the program generation.
As an example, if the linear combination is -2 * p0 + -1 * p1 + 2 * p2,
then a shortest program (among others) might be:
  x3 = p0 + p0
  x4 = p1 + x3
  x5 = p2 + p2
  x6 = - x4
  x7 = x5 + x6
 return x7

Examples of Execution:
  python3
  python3
"""

from pycsp3 import *

print(data)
m, e, n, np, coeffs, rp = data

# lo= VarArray()
