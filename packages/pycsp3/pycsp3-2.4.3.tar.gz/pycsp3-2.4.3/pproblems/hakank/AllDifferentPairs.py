"""
"""

from pycsp3 import *

n = data or 5
m = n * (n - 1) // 2

x = VarArray(size=[m, 2], dom=range(1, n + 1))

satisfy(
    AllDifferent(x[k, 0] * (n - 1) + x[k, 1] for k in range(m)),

    Increasing([x[k, 0] * (n - 1) + x[k, 1] for k in range(m)], strict=True),

    [x[k, 0] != x[k, 1] for k in range(m)]
)

"""
one could introduce an array y for denoting decompositions
"""