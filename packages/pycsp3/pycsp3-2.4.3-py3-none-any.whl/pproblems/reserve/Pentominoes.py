"""
"""

from pycsp3 import *
from pycsp3.classes.auxiliary.enums import TypeSquareSymmetry
from pycsp3.tools.utilities import polyominoes

n, m = data
assert n * m == 60  # for the moment

pentominoes = polyominoes[5].values()


def table(pentomino):
    symmetries = TypeSquareSymmetry.symmetric_patterns(pentomino)
    tbl = []
    for i in range(n):
        for j in range(m):
            for sym in symmetries:
                if all(0 <= i + k < n and 0 <= j + l < m for k, l in sym):
                    tbl.append(tuple((i + k) * m + (j + l) for k, l in sym))
    return tbl


# x[i][j] is the board cell index where is put the jth piece of the ith pentomino
x = VarArray(size=[12, 5], dom=range(n * m))

satisfy(
    # positioning all pentominoes correctly
    [x[i] in table(pentomino) for i, pentomino in enumerate(pentominoes)],

    # ensuring no overlapping pieces
    AllDifferent(x)
)
