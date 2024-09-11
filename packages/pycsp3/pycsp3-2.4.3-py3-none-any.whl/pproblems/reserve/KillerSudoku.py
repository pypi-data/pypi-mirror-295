"""
Problem 057 on CSPLib
"""

from pycsp3 import *
from math import sqrt

n, raw_cages = data  # n (order of the grid) is typically 9
base = int(sqrt(n))
assert base * base == n

# x[i][j] is the value in cell at row i and col j.
x = VarArray(size=[n, n], dom=range(1, n + 1))

cages = [(cage[0], [x[v // n][v % n] for v in cage[1:]]) for cage in raw_cages]

satisfy(
    # imposing distinct values on each row and each column
    AllDifferent(x, matrix=True),

    # imposing distinct values on each block  tag(blocks)
    [AllDifferent(x[i:i + base, j:j + base]) for i in range(0, n, base) for j in range(0, n, base)],

    # each cage must add up to the right value
    [Sum(cells) == v for v, cells in cages],

    # each cage must contain different values
    [AllDifferent(cells) for _, cells in cages]
)
