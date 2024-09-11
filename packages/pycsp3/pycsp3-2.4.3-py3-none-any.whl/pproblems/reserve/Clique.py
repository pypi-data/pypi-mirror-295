"""
Problem 074 CSPLib

The problem is to find a clique of maximum size in a directed graph, specified by its adjacency matrix

Examples of Execution:
  python3 Clique.py -data=cl10.json
"""

from pycsp3 import *

matrix = data
n = len(matrix)

# x[i] is 1 iff the ith node belongs to the clique
x = VarArray(size=n, dom={0, 1})

satisfy(
    # the clique includes at most one of any pair of non-neighbouring vertices
    x[i] + x[j] != 2 for i, j in combinations(n, 2) if matrix[i][j] == matrix[j][i] == 0
)

maximize(
    # maximizing the size of the clique
    Sum(x)
)
