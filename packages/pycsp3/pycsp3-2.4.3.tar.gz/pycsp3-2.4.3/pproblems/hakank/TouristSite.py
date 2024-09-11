"""
From Pierre Flener's presentation "Constraint Technology - A Programming Paradigm on the Rise"
See http://www.it.uu.se/edu/course/homepage/ai/vt08/AI-CT.pdf

With 7 tourist sites and 7 judges:
- Every tourist site is visited by r = 3 judges.
- Every judge visits c = 3 tourist sites.
- Every pair of sites is visited by lambda = 1 common judge.

There are 151200 solutions to this problem.
With the additional constraint that Ali should visit Birka, Falun and Lund, there are 4320 solutions.
"""

from pycsp3 import *

r, c, ld = 3, 3, 1

Birka, Falun, Lund, Mora, Sigtuna, Uppsala, Ystad = sites = range(7)
Ali, Dan, Eva, Jim, Leo, Mia, Ulla = judges = range(7)
nSites, nJudges = len(sites), len(judges)

x = VarArray(size=[nSites, nJudges], dom={0, 1})

satisfy(
    # tag(symmetry-breaking)
    [x[i, Ali] == 1 for i in {Birka, Falun, Lund}],

    # every tourist site is visited by r judges.
    [Sum(x[i]) == r for i in sites],

    # every judge visits c tourist sites.
    [Sum(x[:, j]) == c for j in judges],

    # every pair of sites is visited by lambda common judge.
    [
        Sum(
            both(
                x[i1][j] == 1,
                x[i1][j] == x[i2][j]
            ) for j in judges
        ) == ld for i1, i2 in combinations(nSites, 2)
    ]
)
