"""
Martin Gardner:
 Given n*(n+1) div 2 numbered pool balls in a triangle, is it
 possible to place them so that the number of each ball below
 two balls is the difference of (the number of) those two balls?

There are no solutions for n from 6 to 10
"""

from pycsp3 import *

n = data or 5
k = (n * (n + 1)) // 2

x = VarArray(size=[n, n], dom=lambda i, j: range(1, k + 1) if i < n - j else None)

satisfy(
    AllDifferent(x),

    [x[i][j] == abs(x[i - 1][j] - x[i - 1][j + 1]) for i in range(1, n) for j in range(n - i)],

    # tag(symmetry-breaking)
    x[-2][0] < x[-2][1]
)
