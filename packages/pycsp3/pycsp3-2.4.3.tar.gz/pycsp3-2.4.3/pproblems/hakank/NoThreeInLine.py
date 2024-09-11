"""
See https://en.wikipedia.org/wiki/No-three-in-line_problem

TODO: we must post all sum wrt all possible lines (including slopes with different degrees)
"""

from pycsp3 import *

n = data
m = 3

x = VarArray(size=[n, n], dom={0, 1})

# z = Var(range(2 * n + 1))

satisfy(
    [Sum(x[i]) < m for i in range(n)],
    [Sum(x[:, j]) < m for j in range(n)],

    [Sum(diag) < m for diag in diagonals_down(x)],
    [Sum(diag) < m for diag in diagonals_up(x)],

    2 * n == Sum(x)

)

# maximize(
#     z
# )
