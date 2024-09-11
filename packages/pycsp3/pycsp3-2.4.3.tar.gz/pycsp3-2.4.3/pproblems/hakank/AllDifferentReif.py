"""
"""

from pycsp3 import *

n = data or 4

x = VarArray(size=n, dom=range(n))

b = Var(0, 1)

satisfy(
    b == AllDifferent(x),

    Increasing(x),
)
