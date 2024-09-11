"""
Three coins lie on a table in the order tails, heads, tails.
In precisely three moves, make them face either all heads or all tails.
"""
from pycsp3 import *

n, nMoves = 3, 3
init = [1, 0, 1]

# x[i][j] is the value of the jth coin after the ith move
x = VarArray(size=[nMoves + 1, n], dom={0, 1})

satisfy(
    x[0] == init,

    [Sum(x[i][j] != x[i + 1][j] for j in range(n)) == 1 for i in range(nMoves)],

    Sum(x[-1]) in {0, 3}
)

"""
1) should we introduce a function Hamming so as to be able to write?
    [Hamming(x[i], x[i + 1]) == 1 for i in range(nMoves)],
2) there are 7 solutions
3) More info in cpmpy model
"""
