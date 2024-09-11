"""
Each of the squares in the grid (n by n) can be in one of two states, lit (white)
or unlit (red). If the player clicks on a square then that square and each
orthogonal neighbour will toggle between the two states. Each mouse click
constitutes one move and the objective of the puzzle is to light all
squares in the least number of moves.
"""

from pycsp3 import *

n = data or 5

# x[i,j] is 1 if the player clicks on the square at row i and column j
x = VarArray(size=[n, n], dom={0, 1})

if not variant():
    satisfy(
        # ensuring that all cells are lit
        Sum(x.cross(i, j)) in (1, 3, 5) for i in range(n) for j in range(n)
    )

elif variant("aux"):
    # d[i,j] is the number of pair of neighbors of the square at row i and column j being clicked
    d = VarArray(size=[n, n], dom={0, 1, 2})  # range(n + 1))

    satisfy(
        # ensuring that all cells are lit
        Sum(x.cross(i, j)) - 2 * d[i, j] == 1 for i in range(n) for j in range(n)
    )

minimize(
    Sum(x)
)
