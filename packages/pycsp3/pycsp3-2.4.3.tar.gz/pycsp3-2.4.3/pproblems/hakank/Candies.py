"""
"""

from pycsp3 import *

if data is None:
    n, d = 9, 5
    ratings = [2, 3, 4, 4, 4, 2, 1, 3, 4]
else:
    n, d, s = data
    from random import seed, randrange

    seed(s)
    ratings = [randrange(d) for _ in range(n)]

x = VarArray(size=n, dom=range(d + 1))

satisfy(
    x[i - 1] < x[i] if ratings[i - 1] < ratings[i] else x[i - 1] > x[i] if ratings[i - 1] > ratings[i] else None for i in range(1, n)
)

minimize(
    Sum(x)
)
