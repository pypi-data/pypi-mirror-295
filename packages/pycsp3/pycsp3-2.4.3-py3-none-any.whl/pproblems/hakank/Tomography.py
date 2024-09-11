"""
See discrete_tomography from http://www.hakank.org/common_cp_models
"""

from pycsp3 import *

if isinstance(data, int):  # three examples from the ECLiPSe program
    if data == 0:  # 1 solution
        row_sums = [0, 0, 8, 2, 6, 4, 5, 3, 7, 0, 0]
        col_sums = [0, 0, 7, 1, 6, 3, 4, 5, 2, 7, 0, 0]
    elif data == 1:  # 1 solution
        row_sums = [10, 4, 8, 5, 6]
        col_sums = [5, 3, 4, 0, 5, 0, 5, 2, 2, 0, 1, 5, 1]
    else:  # 3 solutions
        row_sums = [11, 5, 4]
        col_sums = [3, 2, 3, 1, 1, 1, 1, 2, 3, 2, 1]
else:
    row_sums, col_sums = data

n, m = len(row_sums), len(col_sums)

x = VarArray(size=[n, m], dom={0, 1})

satisfy(
    [Sum(x[i]) == row_sums[i] for i in range(n)],

    [Sum(x[:, j]) == col_sums[j] for j in range(m)]
)
