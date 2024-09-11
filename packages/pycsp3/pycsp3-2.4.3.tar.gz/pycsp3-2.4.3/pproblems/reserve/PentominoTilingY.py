"""
Tiling a 10x10 rectangle with 20 Y pentominoes
"""

from pycsp3 import *
from pycsp3.classes.auxiliary.enums import TypeSquareSymmetry
from pycsp3.tools.utilities import polyominoes

n, m = 10, 10
nY = 20

Y = polyominoes[5]["Y"]
symmetries = TypeSquareSymmetry.symmetric_patterns(Y)
print(symmetries)

nSymmetries = len(symmetries)
pivot = round(100 * (nY / nSymmetries))


def table():
    tbl = []
    for i in range(n):
        for j in range(m):
            for p, sym in enumerate(symmetries):
                if all(0 <= i + k < n and 0 <= j + l < m for k, l in sym):
                    tbl.append(tuple([(i + k) * m + (j + l) for k, l in sym] + [p]))
    return tbl


T = table()

# x[i][j] is the board cell index where is put the jth piece of the ith pentomino
x = VarArray(size=[nY, 5], dom=range(n * m))

# y[i] is the form (symmetry variant) of the ith pentomino
y = VarArray(size=nY, dom=range(nSymmetries))

satisfy(
    # positioning all pentominoes correctly
    [(x[i], y[i]) in T for i in range(nY)],

    # ensuring no overlapping pieces
    AllDifferent(x)
)

minimize(
    Sum(abs(100 * Count(y, value=i) - pivot) for i in range(nSymmetries))
)

"""
TODO: detecting mistakes like Count(y, value == i)  // using == instead of = 
"""
