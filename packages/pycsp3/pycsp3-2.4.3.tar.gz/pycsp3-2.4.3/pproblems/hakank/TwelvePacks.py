"""

"""

from pycsp3 import *

sizes, target = data or ([5, 3], 16)
n = len(sizes)

# x[i] is the number of packs of the ith size
x = VarArray(size=n, dom=lambda i: range(target // sizes[i] + 1))

if not variant():

    satisfy(
        x * sizes >= target
    )

    minimize(
        x * sizes - target
    )

elif variant("z"):

    z = Var(range(target * n))

    satisfy(
        z == x * sizes - target
    )

    minimize(
        z
    )
