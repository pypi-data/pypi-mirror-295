"""
From Ozgur Akgun paper
"""

from pycsp3 import *

n = data

n, s = data or (3, 1)
ix = n - 1
max_val = (s - 1) + 3 * n * n - 3 * n + 1
domain = range(s - 1, max_val)
# magic = sum(domain) // (2 * n - 1)
d = n + n - 1  # longest diameter

x = VarArray(size=[d, d, d], dom=range(max_val + 1))

magic = Var(dom=range(sum(domain) + 1))

A, B, C, D, E, F = [x[i + ix][j + ix][k + ix] for (i, j, k) in [(0, ix, -ix), (ix, 0, -ix), (ix, -ix, 0), (-ix, 0, ix), (0, -ix, ix), (-ix, ix, 0)]]

indexes = [(i, j, k) for i in range(d) for j in range(d) for k in range(d)]
used_cells = [(i, j, k) for i, j, k in indexes if i + j + k - 3 * ix == 0]
unused_cells = [(i, j, k) for i, j, k in indexes if i + j + k - 3 * ix != 0]

satisfy(

    [x[i][j][k] != 0 for i, j, k in used_cells],

    [x[i][j][k] == 0 for i, j, k in unused_cells],

    # ensuring all values are different
    AllDifferent(x[i][j][k] for i, j, k in used_cells),

    # ensuring magic sums
    [
        [Sum(x[i]) == magic for i in range(d)],
        [Sum(x[:, j, :]) == magic for j in range(d)],
        [Sum(x[:, :, k]) == magic for k in range(d)]
    ],

    # tag(symmetry-breaking)
    [
        LexIncreasing([A, B, C, D, E, F], [B, C, D, E, F, A]),
        LexIncreasing([A, B, C, D, E, F], [C, D, E, F, A, B]),
        LexIncreasing([A, B, C, D, E, F], [D, E, F, A, B, C]),
        LexIncreasing([A, B, C, D, E, F], [E, F, A, B, C, D]),
        LexIncreasing([A, B, C, D, E, F], [F, A, B, C, D, E]),

        LexIncreasing([A, B, C, D, E, F], [A, F, E, D, C, B]),
        LexIncreasing([A, B, C, D, E, F], [B, A, F, E, D, C]),
        LexIncreasing([A, B, C, D, E, F], [C, B, A, F, E, D]),
        LexIncreasing([A, B, C, D, E, F], [D, C, B, A, F, E]),
        LexIncreasing([A, B, C, D, E, F], [E, D, C, B, A, F]),
        LexIncreasing([A, B, C, D, E, F], [F, E, D, C, B, A])
    ]
)
