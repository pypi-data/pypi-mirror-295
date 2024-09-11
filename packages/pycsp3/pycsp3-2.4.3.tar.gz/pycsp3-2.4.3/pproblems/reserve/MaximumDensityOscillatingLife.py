"""
See Section 8 in "Generating Special-Purpose Stateless Propagators for Arbitrary Constraints"
by Ian P. Gent, Chris Jefferson, Ian Miguel, and Peter Nightingale

for XCSP24 competition
"""

from pycsp3 import *
from pycsp3.classes.auxiliary.enums import TypeSquareSymmetry

n, horizon = data or (5, 5)
symmetries = [sym.apply_on(n + 2) for sym in TypeSquareSymmetry]

# x[t][i][j] is 1 iff the cell at row i and col j is alive at time t
x = VarArray(size=[horizon, n + 2, n + 2], dom=lambda t, i, j: {0} if i in (0, n + 1) or j in (0, n + 1) else {0, 1})

T = ([(ANY, *[0] * 8, 0)] +
     [(ANY, *[1 if k == k1 else 0 for k in range(8)], 0) for k1 in range(8)] +
     [(ANY, *[0 if k in (k1, k2, k3, k4) else 1 for k in range(8)], 0) for k1, k2, k3, k4 in combinations(8, 4)] +
     [(ANY, *[0 if k in (k1, k2, k3) else 1 for k in range(8)], 0) for k1, k2, k3 in combinations(8, 3)] +
     [(ANY, *[0 if k in (k1, k2) else 1 for k in range(8)], 0) for k1, k2 in combinations(8, 2)] +
     [(ANY, *[0 if k == k1 else 1 for k in range(8)], 0) for k1 in range(8)] +
     [(ANY, *[1] * 8, 0)] +
     [(ANY, *[1 if k in (k1, k2, k3) else 0 for k in range(8)], 1) for k1, k2, k3 in combinations(8, 3)] +
     [(0, *[1 if k in (k1, k2) else 0 for k in range(8)], 0) for k1, k2 in combinations(8, 2)] +
     [(1, *[1 if k in (k1, k2) else 0 for k in range(8)], 1) for k1, k2 in combinations(8, 2)]
     )

satisfy(
    # imposing rules of the game
    [(x[t][i][j], x[t].around(i, j), x[(t + 1) % horizon][i][j]) in T for t in range(horizon) for i in range(1, n) for j in range(1, n)],

    # forbidding identical states
    AllDifferentList(x[t] for t in range(horizon)),

    # tag(symmetry-breaking)
    [LexIncreasing(x[0], [[x[0][k][l] for k, l in row] for row in symmetry]) for symmetry in symmetries]
)

maximize(
    # maximizing the number of alive cells
    Sum(x)
)

"""
1) By using 
  [LexIncreasing(x[0], x[i]) for i in range(1, p)],
 together with the already posted symmetry-breaking group, we do not have the same bounds
 It seems that we cannot use these two groups simultaneously (or a bug somewhere?)
"""
