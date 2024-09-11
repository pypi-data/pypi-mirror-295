"""
See Pesant
"""

from pycsp3 import *

forbidden, costs = data
n, m = len(costs), len(costs[0]) - 1  # 4 and 25 for Pesant instances

# x[i,j] is the task performed by the ith employee at time j
x = VarArray(size=[n, m], dom={0, 2, 3, 5})

satisfy(
    [x[i, j] != k for (i, j, k) in forbidden],

    [x[i] * costs[i][:-1] == costs[i][-1] for i in range(n)],

    [AllDifferent(x[:, j]) for j in range(m)]
)
