"""
See https://en.wikipedia.org/wiki/Takuzu
See Hakank

"""

from pycsp3 import *

n, grid = data
assert n % 2 == 0
m = n // 2

# x[i][j] is the value in the cell of the grid at coordinates (i,j)
x = VarArray(size=[n, n], dom={0, 1})

satisfy(
    # ensuring that each row has the same number of 0s and 1s
    [Sum(x[i]) == m for i in range(n)],

    # ensuring that each colum has the same number of 0s and 1s
    [Sum(x[:, j]) == m for j in range(n)],

    # ensuring no more than two adjacent equal values on each row
    [either(x[i][j] != x[i - 1][j], x[i][j] != x[i + 1][j]) for i in range(1, n - 1) for j in range(n)],

    # ensuring no more than two adjacent equal values on each column
    [either(x[i][j] != x[i][j - 1], x[i][j] != x[i][j + 1]) for j in range(1, n - 1) for i in range(n)],

    # forbidding identical rows
    AllDifferentList(x[i] for i in range(n)),

    # forbidding identical columns
    AllDifferentList(x[:, j] for j in range(n)),

    # respecting clues if any
    [x[i][j] == grid[i][j] for i in range(n) for j in range(n) if grid and grid[i][j] != -1]
)

if variant("cop"):
    maximize(
        Sum(x[:10, :10])
    )
