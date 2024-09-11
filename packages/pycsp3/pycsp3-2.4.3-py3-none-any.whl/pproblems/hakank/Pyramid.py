"""
http://www.rosettacode.org/wiki/Pyramid_of_numbers

choco efficient
10-2500 (2144)
11-5000 (4497)
12-10000 (9504)
13-20000 (19872)
14-45000 (41455)
15-80000
"""

from pycsp3 import *

n, k = data

# x[o,p] is the value of A(o,p)
x = VarArray(size=[n, n], dom=lambda i, j: range(k + 1) if j <= i else None)

satisfy(
    x[0][0] != 0,

    AllDifferent(x),

    [x[i][j] == x[i + 1][j] + x[i + 1][j + 1] for i in range(n - 1) for j in range(i + 1)]
)

minimize(
    x[0][0]
)
