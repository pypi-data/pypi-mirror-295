"""
"""

from pycsp3 import *

n, k = data or (5, 1000)
squares = {v * v for v in range(k)}

# x[i] is the ith integer of the series
x = VarArray(size=n, dom=range(k + 1))

p = VarArray(size=[n, n], dom=lambda i, j: squares if i < j else None)

satisfy(
    AllDifferent(x),

    Increasing(x, strict=True),

    [p[i][j] - 1 == x[i] * x[j] for i, j in combinations(n, 2)]
)

if variant("opt"):
    minimize(
        Maximum(x)
    )
