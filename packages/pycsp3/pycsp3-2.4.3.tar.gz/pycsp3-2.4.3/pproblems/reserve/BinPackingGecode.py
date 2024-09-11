"""
See Chapter 20 in Gecode guide
"""

from pycsp3 import *

c = 100
sizes = [99, 98, 95, 95, 95, 94, 94, 91, 88, 87, 86, 85, 76, 74, 73, 71, 68, 60, 55, 54, 51, 45, 42, 40, 39, 39, 36, 34, 33, 32, 32, 31, 31, 30, 29, 26, 26, 23,
         21, 21, 21, 19, 18, 18, 16, 15, 5, 5, 4, 1]
nItems, nBins = len(sizes), 30

assert all(sizes[i] >= sizes[i + 1] for i in range(nItems - 1)), "sizes must be given in decreasing order"

x = VarArray(size=nItems, dom=range(nBins))

if not variant():
    satisfy(
        BinPacking(x, sizes=sizes) <= c
    )

elif variant("dec"):
    satisfy(
        [x[i] == b for i in range(nItems)] * sizes <= c for b in range(nBins)
    )

satisfy(
    # tag(symmetry-breaking)
    [
        Precedence(x),

        [x[i] < x[i + 1] for i in range(nItems - 1) if sizes[i] == sizes[i + 1]],

        [x[i] == i for i in range(nItems) if sizes[i] > c // 2]
    ]
)

minimize(
    Maximum(x)
)

""" Comments
1) using Maximum(x) instead of NValues(x) is far better 
2) AllDifferent(x[i] for i in range(nItems) if sizes[i] > c // 2) is obviously weaker than 
   [x[i] == i for i in range(nItems) if sizes[i] > c // 2]
3) symmetry-breaking constraints are not so important (with the Maximum objective)
  actually, just keeping the Precedence constraint is the most effective choice on this instance (7 wrong decisions)
4) one should replace 30 by a computed upper bound
"""
