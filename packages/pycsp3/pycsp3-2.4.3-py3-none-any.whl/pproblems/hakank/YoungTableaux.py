"""
See  http://mathworld.wolfram.com/YoungTableau.html
     http://en.wikipedia.org/wiki/Young_tableau
"""

from pycsp3 import *

n = data or 4

# x[i][j] is the value in the grid at coordinates (i,j)
x = VarArray(size=[n, n], dom=range(1, n + 2))

# y[i] is the number of values (different from the top value) in the ith row
y = VarArray(size=n, dom=range(n + 1))

satisfy(
    # all values (different from the top value) must occur once
    Cardinality(x, occurrences={i: 1 for i in range(1, n + 1)} + {n + 1: (n * n) - n}),

    # ordering rows
    [Increasing(x[i]) for i in range(n)],

    # ordering columns
    [Increasing(x[:, j]) for j in range(n)],

    # computing the shape
    [y[i] == Sum(x[i][j] <= n for j in range(n)) for i in range(n)],

    # tag(redundant-constraints)
    Sum(y) == n,

    # ordering p
    Decreasing(y)
)
