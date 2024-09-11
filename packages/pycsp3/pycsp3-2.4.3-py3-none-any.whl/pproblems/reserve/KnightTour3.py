"""
See https://en.wikipedia.org/wiki/Knight%27s_tour

Examples of Execution:
  python3 KnightTour2.py
  python3 KnightTour2.py -data=16
"""

from pycsp3 import *

n = data or 8
primes = all_primes(n * n)
selection = sorted(primes + [1, 4, 8, 16, 32, 64])  # primes and powers of 2
print(selection, len(selection))
m = len(selection)


def domain_x(r, c):
    t = [(r - 2, c - 1), (r - 2, c + 1), (r - 1, c - 2), (r - 1, c + 2), (r + 1, c - 2), (r + 1, c + 2), (r + 2, c - 1), (r + 2, c + 1)]
    return {k * n + l for (k, l) in t if 0 <= k < n and 0 <= l < n}


def row(var):
    return var // n


def col(var):
    return var % n


def attacking(v, i, j):
    return (row(v) == i) | (col(v) == j) | (abs(row(v) - i) == abs(col(v) - j))


# x[i][j] is the cell number that comes in the tour (by the knight) after cell (i,j)
x = VarArray(size=[n, n], dom=domain_x)

# y[i][j] is the value in cell (i,j)
# y = VarArray(size=[n, n], dom=range(n * n))

# w[i] is the cell for the i+1th value
w = VarArray(size=n * n, dom=range(n * n))

# q is the cell for the queen
q = Var(dom=range(n * n))

# p[j] is 1 iff the j+1th prime number is attacked by a queen
p = VarArray(size=m, dom={0, 1})

T2 = {(i, j, 0 if (i == j) | (i // n != j // n) & (i % n != j % n) & (abs(i // n - j // n) != abs(i % n - j % n)) else 1) for i in range(n * n) for j in
      range(n * n)}

satisfy(
    # the knights form a circuit (tour)
    Circuit(x),

    [w[x[i][j]] == (w[i * n + j] + 1) % (n * n) for i in range(n) for j in range(n)],

    # computing values
    # [y[x[i][j]] == (y[i][j] + 1) % (n * n) for i in range(n) for j in range(n)],

    # ensuring that prime numbers are attacked by the queen
    [(q, w[k], p[j]) in T2 for j, k in enumerate(p for p in selection)],

    w[0] == 14,

    # y[1][4] == 0,

    # [y[4][2] == 31, y[5][3] == 41, y[6][4] == 59, y[7][4] == 26]
)

maximize(
    # maximizing the number of attacked primes
    Sum(p)
)

# [att[i][j] == belong(y[i][j], primes) & attacking(q, i, j) for i in range(n) for j in range(n)],
