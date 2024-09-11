"""
"""

from pycsp3 import *
from pycsp3.classes.auxiliary.enums import TypeSquareSymmetry
from pycsp3.tools.utilities import polyominoes

n, m = data
assert n * m in (60, 64)  # for the moment

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
    # positioning all pentominoes
    x[i] in table(pentomino) for i, pentomino in enumerate(pentominoes)
)

if n * m == 60:

    satisfy(
        AllDifferent(x)
    )

else:  # n * m == 64

    A = [(0, 0), (0, 1), (1, 0), (1, 1)]  # auxiliary square tetromino

    y = VarArray(size=4, dom=range(n * m))

    satisfy(
        AllDifferent(x + y),

        # putting the tetromino
        y in table(A),

        # setting arbitrarily the pentomino X
        x[9] == (2, 9, 10, 11, 18)
    )

"""
not correct :  # tag(symmetry-breaking)
    [x[0][0] < x[0][-1], x[0][0] < x[-1][0], x[0][0] < x[-1][-1]]
"""
