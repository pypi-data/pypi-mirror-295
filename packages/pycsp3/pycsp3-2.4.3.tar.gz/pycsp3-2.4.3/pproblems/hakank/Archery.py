"""
How close can the young archer come to scoring a total of 100 - using as many arrows as she please.
The targets are: 16, 17, 23, 24, 39, 40
"""

from pycsp3 import *

goal, targets = data or (100, (16, 17, 23, 24, 39, 40))
n, d = len(targets), 100 // min(targets) + 2

x = VarArray(size=n, dom=range(d))

minimize(
    abs(goal - x * targets)
)
