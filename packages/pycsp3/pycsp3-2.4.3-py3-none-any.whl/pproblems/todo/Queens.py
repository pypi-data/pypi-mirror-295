from pycsp3 import *

n = data

# q[i] is the column of the ith queen (at row i)
q = VarArray(size=n, dom=range(n))

satisfy(
    (
        q[i] != q[j],
        abs(q[i] - q[j]) != j - i
    ) for i, j in combinations(n, 2)
)
