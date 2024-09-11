"""
From https://gcanyon.wordpress.com/2009/10/28/a-programming-puzzle-from-einav/
See also einav_puzzle at http://www.hakank.org/common_cp_models
"""

from pycsp3 import *

if isinstance(data, int):
    if data == 0:
        puzzle = [[33, 30, -10], [-16, 19, 9], [-17, -12, -14]]
    else:
        puzzle = [
            [33, 30, 10, -6, 18, -7, -11, 23, -6],
            [16, -19, 9, -26, -8, -19, -8, -21, -14],
            [17, 12, -14, 31, -30, 13, -13, 19, 16],
            [-6, -11, 1, 17, -12, -4, -7, 14, -21],
            [18, -31, 34, -22, 17, -19, 20, 24, 6],
            [33, -18, 17, -15, 31, -5, 3, 27, -3],
            [-18, -20, -18, 31, 6, 4, -2, -12, 24],
            [27, 14, 4, -29, -3, 5, -29, 8, -12],
            [-15, -7, -23, 23, -9, -8, 6, 8, -12],
            [33, -23, -19, -4, -8, -7, 11, -12, 31],
            [-20, 19, -15, -30, 11, 32, 7, 14, -5],
            [-23, 18, -32, -2, -31, -7, 8, 24, 16],
            [32, -4, -10, -14, -6, -1, 0, 23, 23],
            [25, 0, -23, 22, 12, 28, -27, 15, 4],
            [-30, -13, -16, -3, -3, -32, -3, 27, -31],
            [22, 1, 26, 4, -2, -13, 26, 17, 14],
            [-9, -18, 3, -20, -27, -32, -11, 27, 13],
            [-17, 33, -7, 19, -32, 13, -31, -2, -24],
            [-31, 27, -31, -29, 15, 2, 29, -15, 33],
            [-18, -23, 15, 28, 0, 30, -4, 12, -32],
            [-3, 34, 27, -25, -18, 26, 1, 34, 26],
            [-21, -31, -10, -13, -30, -17, -12, -26, 31],
            [23, -31, -19, 21, -17, -10, 2, -23, 23],
            [-3, 6, 0, -3, -32, 0, -10, -25, 14],
            [-19, 9, 14, -27, 20, 15, -5, -27, 18],
            [11, -6, 24, 7, -17, 26, 20, -31, -25],
            [-25, 4, -16, 30, 33, 23, -4, -4, 23]
        ]
else:
    puzzle = data

n, m = len(puzzle), len(puzzle[0])

x = VarArray(size=[n, m], dom=range(-100, 101))

row_sums = VarArray(size=n, dom=range(201))
col_sums = VarArray(size=m, dom=range(201))

row_signs = VarArray(size=n, dom={-1, 1})
col_signs = VarArray(size=m, dom={-1, 1})

satisfy(
    [x[i, j] == puzzle[i][j] * row_signs[i] * col_signs[j] for i in range(n) for j in range(m)],

    [row_sums[i] == Sum(row_signs[i] * col_signs[j] * puzzle[i][j] for j in range(m)) for i in range(n)],

    [col_sums[j] == Sum(row_signs[i] * col_signs[j] * puzzle[i][j] for i in range(n)) for j in range(m)]
)

minimize(
    # minimizing the total sum
    Sum(x)
)
