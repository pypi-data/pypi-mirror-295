"""

"""

from pycsp3 import *

n = data or 8

lb, ub = (n * (n + 1)) // 2, ((n * n) * (n * n + 1)) // 2

# x[i][j] is the value put in cell of the matrix at coordinates (i,j)
x = VarArray(size=[n, n], dom=range(1, n * n + 1))

# rs[i] is the sum of values in the ith row
rs = VarArray(size=n, dom=range(lb, ub + 1))

# cs[j] is the sum of values in the jth column
cs = VarArray(size=n, dom=range(lb, ub + 1))

# ds is the sum in the two diagonals
ds = VarArray(size=2, dom=range(lb, ub + 1))

satisfy(
    # all values must be different
    AllDifferent(x),

    # computing row sums
    [rs[i] == Sum(x[i]) for i in range(n)],

    # computing column sums
    [cs[j] == Sum(x[:, j]) for j in range(n)],

    # computing diagonal sums
    [ds[0] == Sum(diagonal_down(x)), ds[1] == Sum(diagonal_up(x))],

    # all sums must be different
    AllDifferent(rs, cs, ds),

    # ensuring Frenicle standard form  tag(symmetry-breaking)
    [
        x[0][0] < x[0][-1],
        x[0][0] < x[-1][0],
        x[0][0] < x[-1][-1],
        x[0][1] < x[1][0]
    ]
)

"""
1) 3120 solution for n=3
2) not a NP-complete problem (it is trivial to build a solution)
"""
