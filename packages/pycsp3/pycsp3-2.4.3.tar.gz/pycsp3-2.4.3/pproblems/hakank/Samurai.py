"""
Too easy, except for computing all solutions
"""
import math
from pycsp3 import *

n = data
m = math.floor(math.sqrt(n))

x = VarArray(size=n, dom=range(n))

y = VarArray(size=[n, n], dom={0, 1})

satisfy(
    AllDifferent(x),

    [y[i][j] == (x[i] == j) for i in range(n) for j in range(n)],

    [Sum(y[i * m:i * m + m, j * m:j * m + m]) == 1 for i in range(m) for j in range(m)],

    [abs(x[i] - x[i + 1]) >= m for i in range(n - 1)]
)
