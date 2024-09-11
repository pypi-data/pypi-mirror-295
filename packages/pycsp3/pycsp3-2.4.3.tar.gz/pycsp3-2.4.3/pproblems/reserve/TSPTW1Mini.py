"""
See Xavier Gillard, Pierre Schaus:
Large Neighborhood Search with Decision Diagrams. IJCAI 2022: 4754-4760
"""

from pycsp3 import *

distances, windows = data
Earliest, Latest = cp_array(zip(*windows))
horizon = max(Latest) + 1
n = len(distances)

# x[i] is the customer (node) visited in the ith position
x = VarArray(size=n + 1, dom=range(n))

# a[i] is the time when is visited the customer in the ith position
a = VarArray(size=n, dom=range(horizon))

ee = VarArray(size=n, dom=Earliest)

el = VarArray(size=n, dom=Latest)

ea = VarArray(size=n, dom=range(horizon))

dx = VarArray(size=n, dom=distances)

T = [(distances[i][j], i, j) for i in range(n) for j in range(n)]

satisfy(
    #  making it a tour while starting and ending at city 0
    [x[0] == 0, x[-1] == 0, a[0] == 0],

    AllDifferent(x[:-1]),

    # computing times
    [
        [ee[i] == Earliest[x[i]] for i in range(n)],
        [el[i] == Latest[x[i]] for i in range(n)],
        [ea[i] == a[x[i]] for i in range(n)]
    ],

    # computing travelled distances
    [(dx[i], x[i], x[(i + 1) % n]) in T for i in range(n)],

    # enforcing time windows
    [
        [ee[i] <= ea[i] for i in range(n)],
        [ea[i] <= el[i] for i in range(n)],
        [ea[i + 1] >= ea[i] + dx[i] for i in range(n - 1)]
    ]
)

minimize(
    # minimizing travelled distance
    Sum(dx)
)
