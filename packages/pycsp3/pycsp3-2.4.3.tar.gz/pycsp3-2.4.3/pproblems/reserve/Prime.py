"""
Problem P, page 76 on D. Knuth Fascicle 7A
"""

from pycsp3 import *

n = 10
selection = sorted(all_primes(n * n) + [1, 4, 8, 16, 32, 64])

# q is the cell index for the queen
q = Var(dom=range(n * n))

# x[i] is the cell index for the ith value
x = VarArray(size=n * n, dom=range(n * n))


# y[i][j] is the value in cell (i,j)
# y = VarArray(size=[n, n], dom=range(n * n))


def neighbours(r1, c1):
    jumps = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    return [(r1 + r2) * n + c1 + c2 for r2, c2 in jumps if 0 <= r1 + r2 < n and 0 <= c1 + c2 < n]


T1 = {(i, j) for i in range(n * n) for j in neighbours(i // n, i % n)}
T2 = {(i, j) for i in range(n * n) for j in range(n * n)
      if not (i == j or i // n != j // n and i % n != j % n and abs(i // n - j // n) != abs(i % n - j % n))}

satisfy(
    # all values are put in different cells
    AllDifferent(x),

    # ensuring a knight move between two successive values
    [(x[i], x[i + 1]) in T1 for i in range(n * n)],

    # ensuring that selected numbers are attacked by the queen
    [(q, x[k]) in T2 for k in selection],

    # some values are preset
    [x[0] == 14, x[31] == 42, x[41] == 53, x[59] == 64, x[26] == 74],

    # tag(hint)
    [x[11] == 0]

    # [y[x[i] // n][x[i] % n] == i for i in range(n * n)],
)

""" Comments
1) for x[i+1], there is an auto-adjustment of the index, when necessary
"""
