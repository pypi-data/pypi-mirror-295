"""
See Winston - Operations research (pages 393-400)
"""

from pycsp3 import *

if isinstance(data, int):
    if data == 0:
        costs = cp_array([[14, 5, 8, 7], [2, 12, 6, 5], [7, 8, 3, 9], [2, 4, 6, 10]])
else:
    costs = data

n, m = len(costs), len(costs[0])

assert n == m  # we assume here that the problem is balanced

x = VarArray(size=n, dom=range(m))

satisfy(
    AllDifferent(x)
)

minimize(
    # minimizing the total sum
    Sum(costs[i][x[i]] for i in range(n))
)
