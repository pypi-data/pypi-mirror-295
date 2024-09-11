"""
The problem is to find a clique of maximum size in a directed graph, specified by its adjacency matrix

https://en.wikipedia.org/wiki/Aztec_diamond
  2
0 x 1
  3
Examples of Execution:
  python3
"""

from pycsp3 import *

n = data


def n_dominos(k):
    return 6 if k == 2 else n_dominos(k - 1) + 2 * k


nDominos = n_dominos(n)

table3 = [(k, k, ANY) for k in range(nDominos)] + [(k, ANY, k) for k in range(nDominos)]
table5 = [(k, k, ANY, ANY, ANY) for k in range(nDominos)] + [(k, ANY, k, ANY, ANY) for k in range(nDominos)] + \
         [(k, ANY, ANY, k, ANY) for k in range(nDominos)] + [(k, ANY, ANY, ANY, k) for k in range(nDominos)]


def valid(i, j):
    if i < 0 or i >= n * 2 or j < 0 or j >= n * 2:
        return False
    if i < n - 1 and (j < n - 1 - i or j > n + i):
        return False
    if i > n and (j < i - n or j > 3 * n - i - 1):
        return False
    return True


def top_left(i, j):
    return valid(i, j) and not valid(i, j - 1) and not valid(i - 1, j)


def top_right(i, j):
    return valid(i, j) and not valid(i, j + 1) and not valid(i - 1, j)


def bot_left(i, j):
    return valid(i, j) and not valid(i, j - 1) and not valid(i + 1, j)


def bot_right(i, j):
    return valid(i, j) and not valid(i, j + 1) and not valid(i + 1, j)


x = VarArray(size=[2 * n, 2 * n], dom=lambda i, j: range(nDominos) if valid(i, j) else None)

m = [[x[i][j]] + [x[k][l] for k, l in [(i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j)] if valid(k, l)] for i in range(2 * n) for j in range(2 * n) if
     valid(i, j)]
scp3, scp5 = [t for t in m if len(t) == 3], [t for t in m if len(t) == 5]

satisfy(
    [scp in table3 for scp in scp3],

    [scp in table5 for scp in scp5],

    Cardinality(x, occurrences={k: 2 for k in range(nDominos)})
)

# symmetry-breaking : [Increasing(x[i]) for i in range(2 * n)] [Increasing(x[:, i]) for i in range(2 * n)],
# but not all symmtries

for i in range(n * 2):
    print(
        ['tl' if top_left(i, j) else 'tr' if top_right(i, j) else 'bl' if bot_left(i, j) else 'br' if bot_right(i, j) else '*' if valid(i, j) else ' ' for j in
         range(n * 2)])
