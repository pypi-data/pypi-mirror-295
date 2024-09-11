"""
"""

from pycsp3 import *

# x[i] is 1 iff the ith node belongs to the clique
x = VarArray(size=10, dom={0, 1})

satisfy(
    Sum(x) // 24 < 10,

    Sum(Sum(x) for _ in range(3)) == 4
)
