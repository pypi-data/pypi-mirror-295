"""
"""

from pycsp3 import *

n, m, d, k = data or (9, 4, 3, 3)

# x[i][j] is the jth value of the ith vector
x = VarArray(size=[n, m], dom=range(d))

satisfy(
    # ensuring a Hamming distance of at least 'k' between any two vectors
    [Hamming(row1, row2) >= k for row1, row2 in combinations(x, 2)],

    # tag(symmetry-breaking)
    LexIncreasing(x)
)

"""
72 solutions for n=9 (and no solution for n=10)
"""
