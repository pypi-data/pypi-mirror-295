"""
362880 different solutions of n=10
"""

from pycsp3 import *

n = data or 5

# x[i] is the node following the ith node
x = VarArray(size=n, dom=range(n))

if not variant():
    satisfy(
        Circuit(x, size=n)
    )

elif variant("dec"):
    z = VarArray(size=n, dom=range(n))

    satisfy(
        AllDifferent(x),
        AllDifferent(z),

        # putting the orbit of x[0] in in z[1..n]
        z[0] == x[0],

        [z[i] == x[z[i - 1]] for i in range(1, n - 1)],

        # forbidding 0 for 0 < i < n-1
        [z[i] != 0 for i in range(1, n - 1)],

        # setting 0 for i = n-1
        z[n - 1] == 0
    )
