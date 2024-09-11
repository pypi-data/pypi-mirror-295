"""
See CP'23 paper

java ace FastMatrixMultiplication-2-2-2-7.xml -ea -eqm
"""

from pycsp3 import *
from pycsp3.classes.main.annotations import ValHeuristic

n, m, p, R = data or (2, 2, 2, 7)
U, V, W = n * m, m * p, n * p

T = []
for k in range(n * p):
    M = [[0] * V for _ in range(U)]
    i, j = k // p, k % p
    for a in range(m):
        M[i * m + a][j + (p * a)] = 1
    T.append(M)

x = VarArray(size=[U, R], dom={-1, 0, 1})

y = VarArray(size=[V, R], dom={-1, 0, 1})

z = VarArray(size=[W, R], dom={-1, 0, 1})

if not variant():

    satisfy(
        [Sum(x[i][r] * y[j][r] * z[k][r] for r in range(R)) == T[k][i][j] for i in range(U) for j in range(V) for k in range(W)],

        # tag(symmetry-breaking)
        [
            [LexIncreasing(x[:, r] + y[:, r], x[:, r + 1] + y[:, r + 1]) for r in range(R - 1)],

            [Precedence(x[:, r], values=[-1, 1]) for r in range(R)],

            [Precedence(z[:, r], values=[-1, 1]) for r in range(R)]
        ]
    )

elif variant("table"):
    T1 = [
        (0, ANY, ANY, 0),
        (ANY, 0, ANY, 0),
        (ANY, ANY, 0, 0),
        (-1, -1, -1, -1),
        (-1, -1, 1, 1),
        (-1, 1, -1, 1),
        (-1, 1, 1, -1),
        (1, -1, -1, 1),
        (1, -1, 1, -1),
        (1, 1, -1, -1),
        (1, 1, 1, 1)]


    def T2(v):
        assert v in (-1, 0, 1)
        return [
            t for t in product((-1, 0, 1), repeat=15) if sum(t) == v
        ]


    # T2s = {0: T2(0), 1: T2(1)}
    # # for q in T2s:
    # #     print("qqqqqqq", T2s[q])
    # print("ok")

    aux = VarArray(size=[U, V, W, R], dom={-1, 0, 1})

    satisfy(
        [(x[i][r], y[j][r], z[k][r], aux[i][j][k][r]) in T1 for i in range(U) for j in range(V) for k in range(W) for r in range(R)],

        # [aux[i][j][k] in T2s[T[k][i][j]] for i in range(U) for j in range(V) for k in range(W)]
        [Sum(aux[i][j][k]) == T[k][i][j] for i in range(U) for j in range(V) for k in range(W)]
    )

annotate(
    valHeuristic=ValHeuristic().static(flatten(x, y, z), order=[0, -1, 1])
)
