"""
Three jugs problem modelled as a shortest path problem.
See Problem from Taha "Introduction to Operations Research", page 245f
"""

from pycsp3 import *

n = 15  # 0 and 14 are start and end nodes
M = 999  # large number

d = [
    [M, 1, M, M, M, M, M, M, 1, M, M, M, M, M, M],
    [M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M],
    [M, M, M, 1, M, M, M, M, 1, M, M, M, M, M, M],
    [M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M],
    [M, M, M, M, M, 1, M, M, 1, M, M, M, M, M, M],
    [M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M],
    [M, M, M, M, M, M, M, 1, 1, M, M, M, M, M, M],
    [M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1],
    [M, M, M, M, M, M, M, M, M, 1, M, M, M, M, M],
    [M, 1, M, M, M, M, M, M, M, M, 1, M, M, M, M],
    [M, M, M, M, M, M, M, M, M, M, M, 1, M, M, M],
    [M, 1, M, M, M, M, M, M, M, M, M, M, 1, M, M],
    [M, M, M, M, M, M, M, M, M, M, M, M, M, 1, M],
    [M, 1, M, M, M, M, M, M, M, M, M, M, M, M, 1],
    [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M]
]

rhs = [1] + [0] * (n - 2) + [-1]  # requirements (right hand statement)

x = VarArray(size=[n, n], dom={0, 1})  # the resulting matrix, 1 if connected, 0 else

outFlow = VarArray(size=n, dom={0, 1})

inFlow = VarArray(size=n, dom={0, 1})

satisfy(
    # outflow constraint
    [outFlow[i] == Sum(x[i][j] for j in range(n) if d[i][j] < M) for i in range(n)],

    # inflow constraint
    [inFlow[j] == Sum(x[i][j] for i in range(n) if d[i][j] < M) for j in range(n)],

    #  inflow = outflow
    [outFlow[i] - inFlow[i] == rhs[i] for i in range(n)]
)

minimize(
    Sum(d[i][j] * x[i][j] for i in range(n) for j in range(n) if d[i][j] < M)
)
