"""
"""

from pycsp3 import *
from collections import Counter

m = data or 10
n = m * 2
t = cp_array(1, -1)

x = VarArray(size=n, dom={0, 1})

c = VarArray(size=n, dom=range(n + 1))

satisfy(
    [x[0] == 0, c[0] == 1],  # start

    [c[i] == c[i - 1] + t[x[i]] for i in range(1, n)],

    [x[-1] == 1, c[-1] == 0]  # end
)

"""
"""
