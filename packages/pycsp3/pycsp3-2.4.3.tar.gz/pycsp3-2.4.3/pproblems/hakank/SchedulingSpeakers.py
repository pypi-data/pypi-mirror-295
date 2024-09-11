"""
From Rina Dechter, Constraint Processing, page 72
Scheduling of 6 speakers in 6 slots.
"""

from pycsp3 import *

n = 6  # number of speakers

available = [
    [3, 4, 5, 6],  # 2) the only one with 6 after speaker F -> 1
    [3, 4],  # 5) 3 or 4
    [2, 3, 4, 5],  # 3) only with 5 after F -> 1 and A -> 6
    [2, 3, 4],  # 4) only with 2 after C -> 5 and F -> 1
    [3, 4],  # 5) 3 or 4
    [1, 2, 3, 4, 5, 6]  # 1) the only with 1
]

x = VarArray(size=n, dom=range(1, n + 1))

satisfy(
    AllDifferent(x),

    [x[i] in available[i] for i in range(n)]
)
