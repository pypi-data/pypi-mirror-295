"""
"""

from pycsp3 import *

n, m = 4, 10

x = VarArray(size=n, dom=range(1, m + 1))

satisfy(
    AllDifferent(x),

    Maximum(x) - Minimum(x) == n - 1
)
