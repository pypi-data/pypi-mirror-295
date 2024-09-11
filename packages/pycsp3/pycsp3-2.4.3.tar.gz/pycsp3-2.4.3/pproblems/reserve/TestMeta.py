from pycsp3 import *

x = VarArray(size=4, dom=range(4))
y = Var(range(-1, 4))

satisfy(
    Or(Sum(x) > 10, AllDifferent(x)),

    If(y != -1, Then=x[y] == 1, meta=True)
)
